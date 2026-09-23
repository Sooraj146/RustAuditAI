import json
import os
import re
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class StatementSummary:
    kind: str
    code: str
    has_clone: bool = False
    has_unsafe: bool = False
    has_allocation: bool = False
    line_number: int = 0


@dataclass
class FunctionAstInfo:
    name: str
    visibility: str = "pub"
    is_unsafe: bool = False
    is_async: bool = False
    inputs: List[str] = field(default_factory=list)
    output_type: str = "()"
    line_start: int = 1
    line_end: int = 1
    clone_count: int = 0
    unsafe_block_count: int = 0
    allocation_count: int = 0
    loop_count: int = 0
    branch_count: int = 0
    borrow_count: int = 0
    statements: List[StatementSummary] = field(default_factory=list)


@dataclass
class AnalysisResult:
    success: bool
    error: Optional[str] = None
    file_path: Optional[str] = None
    functions: List[FunctionAstInfo] = field(default_factory=list)



class RustParser:
    """
    Rust parser bridge for RustAuditAI.
    Tries the native `cargo_parser` Rust binary first; falls back to internal Python
    regex-ast parser if Rust binary is unavailable or in sandboxed execution environments.
    """

    def __init__(self, binary_path: Optional[str] = None):
        if binary_path:
            self.binary_path = Path(binary_path)
        else:
            base = Path(__file__).parent.parent.parent / "cargo_parser" / "target" / "release" / "cargo_parser.exe"
            if not base.exists():
                base = Path(__file__).parent.parent.parent / "cargo_parser" / "target" / "debug" / "cargo_parser.exe"
            self.binary_path = base

    def parse_file(self, file_path: str) -> AnalysisResult:
        path = Path(file_path)
        if not path.exists():
            return AnalysisResult(success=False, error=f"File not found: {file_path}", file_path=file_path)

        code = path.read_text(encoding="utf-8")
        return self.parse_code(code, file_path=str(path))

    def parse_code(self, code: str, file_path: Optional[str] = None) -> AnalysisResult:
        # Try native cargo_parser binary if executable exists
        if self.binary_path.exists():
            try:
                res = subprocess.run(
                    [str(self.binary_path)],
                    input=code,
                    text=True,
                    capture_output=True,
                    timeout=10,
                )
                if res.returncode == 0 and res.stdout.strip():
                    data = json.loads(res.stdout)
                    if not data.get("success", True):
                        fallback = self._python_fallback_parse(code, file_path=file_path)
                        if fallback.success and fallback.functions:
                            return fallback
                        return AnalysisResult(
                            success=False,
                            error=data.get("error") or "Rust syntax error",
                            file_path=data.get("file_path", file_path),
                            functions=[],
                        )
                    fns = []
                    for f in data.get("functions", []):
                        stmts = [StatementSummary(**s) for s in f.get("statements", [])]
                        f["statements"] = stmts
                        fn_obj = FunctionAstInfo(**f)
                        if fn_obj.line_start == 0:
                            m = re.search(r'\bfn\s+' + re.escape(fn_obj.name) + r'\b', code)
                            if m:
                                fn_obj.line_start = code[:m.start()].count('\n') + 1
                                _, _, fn_obj.line_end = self._extract_block(code, m.start(), code.splitlines())
                        fns.append(fn_obj)

                    if fns:
                        self._resolve_statement_lines(code, fns)
                        return AnalysisResult(
                            success=True,
                            error=None,
                            file_path=data.get("file_path", file_path),
                            functions=fns,
                        )

            except Exception:
                pass

        # Fallback Python AST parser
        return self._python_fallback_parse(code, file_path=file_path)

    def _python_fallback_parse(self, code: str, file_path: Optional[str] = None) -> AnalysisResult:
        """
        Pure Python fallback parser extracting function-level ASTs, statements, and indicators.
        """
        functions: List[FunctionAstInfo] = []
        lines = code.splitlines()

        # Regex pattern for Rust functions
        fn_pattern = re.compile(
            r'(?P<vis>pub(?:\([\w\s]+\))?\s+)?'
            r'(?P<unsafe>unsafe\s+)?'
            r'(?P<async>async\s+)?'
            r'fn\s+(?P<name>\w+)\s*'
            r'\((?P<args>[^)]*)\)'
            r'(?:\s*->\s*(?P<ret>[^{]+))?'
            r'\s*\{'
        )

        for match in fn_pattern.finditer(code):
            fn_name = match.group('name')
            vis = (match.group('vis') or '').strip() or 'private'
            is_unsafe = bool(match.group('unsafe'))
            is_async = bool(match.group('async'))
            args_str = (match.group('args') or '').strip()
            ret_type = (match.group('ret') or '').strip() or '()'

            inputs = [arg.strip() for arg in args_str.split(',') if arg.strip()]

            # Extract body block
            start_pos = match.end() - 1
            body_code, line_start, line_end = self._extract_block(code, start_pos, lines)

            # Analyze function metrics
            clone_count = len(re.findall(r'\.clone\s*\(', body_code))
            unsafe_block_count = len(re.findall(r'\bunsafe\s*\{', body_code))
            alloc_count = len(re.findall(r'\b(?:Box::new|Vec::new|String::from|Rc::new|Arc::new|\.to_vec|\.to_string|\.to_owned)\b', body_code))
            loop_count = len(re.findall(r'\b(?:loop|while|for\s+\w+\s+in)\b', body_code))
            branch_count = len(re.findall(r'\b(?:if|match|else\s+if)\b', body_code))
            borrow_count = len(re.findall(r'&\s*mut\b|&\s*(?![&|=])', body_code))

            statements = self._extract_statements(body_code)

            fn_info = FunctionAstInfo(
                name=fn_name,
                visibility=vis,
                is_unsafe=is_unsafe,
                is_async=is_async,
                inputs=inputs,
                output_type=ret_type,
                line_start=line_start,
                line_end=line_end,
                clone_count=clone_count,
                unsafe_block_count=unsafe_block_count,
                allocation_count=alloc_count,
                loop_count=loop_count,
                branch_count=branch_count,
                borrow_count=borrow_count,
                statements=statements,
            )
            functions.append(fn_info)

        if not functions:
            return AnalysisResult(
                success=False,
                error="No Rust functions detected. Please provide a valid Rust subroutine (e.g. `fn my_function() { ... }`).",
                file_path=file_path,
                functions=[],
            )

        self._resolve_statement_lines(code, functions)
        return AnalysisResult(
            success=True,
            error=None,
            file_path=file_path,
            functions=functions,
        )

    def _extract_block(self, code: str, start_index: int, lines: List[str]) -> tuple[str, int, int]:
        depth = 0
        end_index = start_index
        for idx in range(start_index, len(code)):
            char = code[idx]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end_index = idx + 1
                    break

        block_code = code[start_index:end_index]
        line_start = code[:start_index].count('\n') + 1
        line_end = code[:end_index].count('\n') + 1
        return block_code, line_start, line_end

    def _extract_statements(self, body_code: str) -> List[StatementSummary]:
        stmts = []
        raw_stmts = [s.strip() for s in body_code.strip('{}').split(';') if s.strip()]
        for stmt_str in raw_stmts:
            kind = "LocalLet" if stmt_str.startswith("let ") else "Expr"
            has_clone = ".clone(" in stmt_str
            has_unsafe = "unsafe" in stmt_str
            has_alloc = any(kw in stmt_str for kw in ["Box::new", "Vec::new", "String::from", ".to_vec", ".to_string"])

            stmts.append(
                StatementSummary(
                    kind=kind,
                    code=stmt_str,
                    has_clone=has_clone,
                    has_unsafe=has_unsafe,
                    has_allocation=has_alloc,
                )
            )
        return stmts

    def _resolve_statement_lines(self, code: str, functions: List[FunctionAstInfo]) -> None:
        """
        Maps each statement to its exact 1-based source line number within the function scope.
        """
        lines = code.splitlines()
        for fn in functions:
            fn_start = max(1, fn.line_start)
            fn_end = min(len(lines), fn.line_end) if fn.line_end >= fn_start else len(lines)
            fn_lines = lines[fn_start - 1 : fn_end]

            curr_search_idx = 0
            for stmt in fn.statements:
                if stmt.line_number > 0:
                    continue

                target_tokens = [t for t in re.findall(r'\b\w+\b', stmt.code) if t not in ('let', 'mut', 'pub', 'fn')]
                matched_offset = curr_search_idx

                if target_tokens:
                    primary_token = target_tokens[0]
                    for offset in range(curr_search_idx, len(fn_lines)):
                        if primary_token in fn_lines[offset]:
                            matched_offset = offset
                            break

                stmt.line_number = fn_start + matched_offset
                curr_search_idx = matched_offset

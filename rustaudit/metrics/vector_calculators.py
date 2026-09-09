"""
Quality Vector Calculator for RustAuditAI.
Evaluates 4 core analytical quality vectors: Safety, Performance, Maintainability, and Security.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from rustaudit.parser.rust_parser import FunctionAstInfo
from rustaudit.graph.cpg_builder import CodePropertyGraph


from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from rustaudit.parser.rust_parser import FunctionAstInfo, StatementSummary
from rustaudit.graph.cpg_builder import CodePropertyGraph
from rustaudit.cwe import CWERegistry, CWEDefinition


@dataclass
class VectorDeduction:
    """
    Standardized quality deduction record tagged with MITRE CWE identification,
    exact statement source location, and actionable remediation advice.
    """
    vector: str           # "safety", "performance", "maintainability", "security"
    cwe_id: str           # e.g. "CWE-119"
    cwe_name: str         # e.g. "Improper Restriction of Operations within the Bounds of a Memory Buffer"
    cwe_url: str          # official MITRE link
    severity: str         # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    penalty: float        # deduction points
    message: str          # human-readable deduction text
    line_number: Optional[int] = None
    statement_code: Optional[str] = None
    remediation: str = ""

    @property
    def description(self) -> str:
        return self.message

    @property
    def url(self) -> str:
        return self.cwe_url

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vector": self.vector,
            "cwe_id": self.cwe_id,
            "cwe_name": self.cwe_name,
            "name": self.cwe_name,
            "cwe_url": self.cwe_url,
            "url": self.cwe_url,
            "severity": self.severity,
            "penalty": self.penalty,
            "message": self.message,
            "description": self.message,
            "line_number": self.line_number,
            "statement_code": self.statement_code,
            "remediation": self.remediation,
        }


@dataclass
class VectorScores:
    safety: float
    performance: float
    maintainability: float
    security: float
    deductions: Dict[str, List[str]] = field(default_factory=dict)
    structured_deductions: List[VectorDeduction] = field(default_factory=list)


class QualityVectorCalculator:
    """
    Computes mathematical quality vector scores (0-100) for a subroutine based on its CPG and AST attributes,
    tagging each identified weakness with MITRE CWE indices and statement line numbers.
    """

    def calculate_vectors(self, fn_info: FunctionAstInfo, cpg: CodePropertyGraph) -> VectorScores:
        deductions: Dict[str, List[str]] = {
            "safety": [],
            "performance": [],
            "maintainability": [],
            "security": [],
        }
        structured_deductions: List[VectorDeduction] = []

        def add_deduction(
            vector: str,
            cwe_id: str,
            penalty: float,
            message: str,
            line_number: Optional[int] = None,
            statement_code: Optional[str] = None,
            severity_override: Optional[str] = None,
            custom_remediation: Optional[str] = None,
        ):
            cwe_def = CWERegistry.get_definition(cwe_id)
            cwe_name = cwe_def.name if cwe_def else "Security Weakness"
            cwe_url = cwe_def.url if cwe_def else f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html"
            severity = severity_override or (cwe_def.default_severity if cwe_def else "MEDIUM")
            remediation = custom_remediation or (cwe_def.remediation if cwe_def else "Refactor to idiomatic Rust.")

            # Formatted log string for backwards compatibility
            loc_str = f" [Line {line_number}]" if line_number else ""
            deductions[vector].append(f"[{cwe_id}{loc_str}] {message} (-{penalty:.1f} pts)")

            structured_deductions.append(
                VectorDeduction(
                    vector=vector,
                    cwe_id=cwe_id,
                    cwe_name=cwe_name,
                    cwe_url=cwe_url,
                    severity=severity,
                    penalty=penalty,
                    message=message,
                    line_number=line_number,
                    statement_code=statement_code,
                    remediation=remediation,
                )
            )

        # 1. Safety Vector Calculation
        safety_score = 100.0
        if fn_info.is_unsafe:
            safety_score -= 30.0
            add_deduction(
                vector="safety",
                cwe_id="CWE-676",
                penalty=30.0,
                message="Function marked with `unsafe` keyword, disabling compiler safety checks",
                line_number=fn_info.line_start,
                statement_code=f"unsafe fn {fn_info.name}",
                severity_override="CRITICAL",
            )

        if fn_info.unsafe_block_count > 0:
            penalty = fn_info.unsafe_block_count * 15.0
            safety_score -= penalty
            first_unsafe_stmt = next((s for s in fn_info.statements if s.has_unsafe or "unsafe" in s.code), None)
            add_deduction(
                vector="safety",
                cwe_id="CWE-119",
                penalty=penalty,
                message=f"Contains {fn_info.unsafe_block_count} explicit `unsafe {{}}` block(s)",
                line_number=first_unsafe_stmt.line_number if first_unsafe_stmt else fn_info.line_start,
                statement_code=first_unsafe_stmt.code if first_unsafe_stmt else None,
                severity_override="HIGH",
            )

        for stmt in fn_info.statements:
            if "as_ptr(" in stmt.code or "as_mut_ptr(" in stmt.code or ("*" in stmt.code and "ptr" in stmt.code):
                safety_score -= 10.0
                add_deduction(
                    vector="safety",
                    cwe_id="CWE-476",
                    penalty=10.0,
                    message=f"Raw pointer operation detected in `{stmt.code[:45]}`",
                    line_number=stmt.line_number,
                    statement_code=stmt.code,
                    severity_override="HIGH",
                )

        safety_score = max(0.0, min(100.0, safety_score))

        # 2. Performance Vector Calculation
        performance_score = 100.0
        if fn_info.clone_count > 0:
            penalty = fn_info.clone_count * 15.0
            performance_score -= penalty
            first_clone_stmt = next((s for s in fn_info.statements if s.has_clone or ".clone(" in s.code), None)
            add_deduction(
                vector="performance",
                cwe_id="CWE-400",
                penalty=penalty,
                message=f"Contains {fn_info.clone_count} `.clone()` call(s) causing redundant heap memory duplication",
                line_number=first_clone_stmt.line_number if first_clone_stmt else fn_info.line_start,
                statement_code=first_clone_stmt.code if first_clone_stmt else None,
                severity_override="MEDIUM",
            )

        if fn_info.allocation_count > 0:
            penalty = fn_info.allocation_count * 10.0
            performance_score -= penalty
            first_alloc_stmt = next((s for s in fn_info.statements if s.has_allocation or any(k in s.code for k in ("Box::new", "Vec::new", "String::from"))), None)
            add_deduction(
                vector="performance",
                cwe_id="CWE-400",
                penalty=penalty,
                message=f"Contains {fn_info.allocation_count} micro-heap allocation(s) (`Box::new`, `Vec::new`, `String::from`)",
                line_number=first_alloc_stmt.line_number if first_alloc_stmt else fn_info.line_start,
                statement_code=first_alloc_stmt.code if first_alloc_stmt else None,
                severity_override="MEDIUM",
            )

        if fn_info.loop_count > 0 and fn_info.allocation_count > 0:
            performance_score -= 15.0
            first_loop_stmt = next((s for s in fn_info.statements if "for " in s.code or "while " in s.code or "loop" in s.code), None)
            add_deduction(
                vector="performance",
                cwe_id="CWE-770",
                penalty=15.0,
                message="Heap allocations performed inside loop structures, degrading memory bandwidth",
                line_number=first_loop_stmt.line_number if first_loop_stmt else fn_info.line_start,
                statement_code=first_loop_stmt.code if first_loop_stmt else None,
                severity_override="HIGH",
            )

        performance_score = max(0.0, min(100.0, performance_score))

        # 3. Maintainability Vector Calculation
        maintainability_score = 100.0
        cc = cpg.cfg.graph.get("cyclomatic_complexity", 1)

        if cc > 10:
            penalty = (cc - 10) * 10.0 + 25.0
            maintainability_score -= penalty
            add_deduction(
                vector="maintainability",
                cwe_id="CWE-710",
                penalty=penalty,
                message=f"High McCabe Cyclomatic Complexity V(G)={cc} (>10 threshold)",
                line_number=fn_info.line_start,
                severity_override="HIGH",
            )
        elif cc > 5:
            penalty = (cc - 5) * 5.0
            maintainability_score -= penalty
            add_deduction(
                vector="maintainability",
                cwe_id="CWE-710",
                penalty=penalty,
                message=f"Moderate Cyclomatic Complexity V(G)={cc} (>5 threshold)",
                line_number=fn_info.line_start,
                severity_override="MEDIUM",
            )

        line_count = fn_info.line_end - fn_info.line_start + 1
        if line_count > 50:
            maintainability_score -= 20.0
            add_deduction(
                vector="maintainability",
                cwe_id="CWE-710",
                penalty=20.0,
                message=f"Subroutine length exceeds 50 lines ({line_count} lines)",
                line_number=fn_info.line_start,
                severity_override="LOW",
            )

        if len(fn_info.statements) > 12:
            maintainability_score -= 10.0
            add_deduction(
                vector="maintainability",
                cwe_id="CWE-710",
                penalty=10.0,
                message=f"High statement density ({len(fn_info.statements)} statements)",
                line_number=fn_info.line_start,
                severity_override="LOW",
            )

        maintainability_score = max(0.0, min(100.0, maintainability_score))

        # 4. Security Vector Calculation
        security_score = 100.0
        for stmt in fn_info.statements:
            if ".unwrap(" in stmt.code or ".expect(" in stmt.code:
                security_score -= 12.0
                add_deduction(
                    vector="security",
                    cwe_id="CWE-252",
                    penalty=12.0,
                    message=f"Unhandled panic risk in `{stmt.code[:45]}` via `.unwrap()` / `.expect()`",
                    line_number=stmt.line_number,
                    statement_code=stmt.code,
                    severity_override="MEDIUM",
                )

        for stmt in fn_info.statements:
            if "[" in stmt.code and "]" in stmt.code and "get(" not in stmt.code:
                security_score -= 10.0
                add_deduction(
                    vector="security",
                    cwe_id="CWE-129",
                    penalty=10.0,
                    message=f"Direct array/slice indexing in `{stmt.code[:45]}` without defensive `.get()` bounds check",
                    line_number=stmt.line_number,
                    statement_code=stmt.code,
                    severity_override="MEDIUM",
                )

        if fn_info.is_unsafe or fn_info.unsafe_block_count > 0:
            security_score -= 15.0
            add_deduction(
                vector="security",
                cwe_id="CWE-119",
                penalty=15.0,
                message="Unsafe block exposes defensive security boundaries to unchecked memory operations",
                line_number=fn_info.line_start,
                severity_override="HIGH",
            )

        security_score = max(0.0, min(100.0, security_score))

        return VectorScores(
            safety=safety_score,
            performance=performance_score,
            maintainability=maintainability_score,
            security=security_score,
            deductions=deductions,
            structured_deductions=structured_deductions,
        )

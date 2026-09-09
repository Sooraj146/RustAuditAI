"""
XAI Prompt Builder for RustAuditAI.
Constructs deterministic, graph-bounded prompt payloads for LLM text reasoning layers.
"""

from typing import Dict, Any, List
from rustaudit.parser.rust_parser import FunctionAstInfo
from rustaudit.graph.cpg_builder import CodePropertyGraph
from rustaudit.metrics.rqi_synthesizer import RQISummary


class XAIPromptBuilder:
    """
    Constructs bounded prompt messages constraining LLM explanations strictly to CPG facts
    and instructing the LLM to generate idiomatic refactorings achieving ~100% RQI.
    """

    SYSTEM_PROMPT = (
        "You are RustAuditAI, an elite Explainable AI static analysis and automated refactoring engine for Rust.\n"
        "Your task is to analyze the provided deterministic Code Property Graph (CPG) facts, ownership graph (FLOG), and Rust Quality Index (RQI) metrics for a Rust function, and generate an explanation and an idiomatic refactored version that achieves near 100% RQI while strictly preserving original functionality.\n\n"
        "CRITICAL RQI REFACTORING GUIDELINES:\n"
        "1. STRICT FUNCTIONAL INVARIANCE: The refactored code MUST preserve the exact runtime behavior, inputs, outputs, and functionality of the original subroutine.\n"
        "2. FUNCTION DECOMPOSITION: If the subroutine has multiple responsibilities, branches, or allocations, decompose it into smaller, well-scoped helper functions. Keep Cyclomatic Complexity V(G) <= 5 and statement count <= 12 in every function for maximum maintainability.\n"
        "3. 100% SAFETY TARGET: Eliminate all `unsafe` keywords, `unsafe { ... }` blocks, and raw pointer invocations (`.as_ptr()`, `.as_mut_ptr()`). Use safe standard library idioms, safe references (`&T`), and safe pointer formatting (e.g. `println!(\"address: {:p}\", data)`).\n"
        "4. 100% PERFORMANCE TARGET: Eliminate all redundant `.clone()` calls. Eliminate unnecessary heap allocations (`Box::new`, `Vec::new`, intermediate `.to_string()`, `.to_owned()`). Never allocate memory inside loops. Prefer zero-cost borrowing (`&str`, `&[T]`) and construct return values cleanly without redundant intermediate buffers.\n"
        "5. 100% SECURITY TARGET: Replace `.unwrap()` and `.expect()` with robust error handling (`match`, `if let`, `?`, `.unwrap_or()`). Replace unchecked slice indexing (`arr[i]`) with defensive bounds-checked access (`arr.get(i)`).\n"
        "6. COMPLETE CODE BLOCK: Section 2 MUST contain the entire standalone, compilable Rust code including the primary refactored function and any decomposed helper functions."
    )

    def build_prompt(
        self,
        fn_info: FunctionAstInfo,
        cpg: CodePropertyGraph,
        rqi_summary: RQISummary,
        original_code: str,
    ) -> str:
        summary = cpg.summary()
        all_deductions = [d for sublist in rqi_summary.vectors.deductions.values() for d in sublist]

        prompt_lines = [
            f"=== TARGET RUST FUNCTION TO REFACTOR: `{fn_info.name}` ===",
            "```rust",
            original_code.strip(),
            "```\n",
            "=== DETERMINISTIC CODE PROPERTY GRAPH (CPG) FACTS ===",
            f"- AST Hierarchy: {summary['ast_nodes']} nodes, {summary['ast_edges']} edges",
            f"- CFG Control Flow: {summary['cfg_nodes']} nodes, {summary['cfg_edges']} edges | McCabe Cyclomatic Complexity V(G) = {summary['cyclomatic_complexity']}",
            f"- FLOG Ownership Graph: {summary['flog_nodes']} nodes, {summary['flog_edges']} edges",
            f"- Total Micro-Heap Allocations: {summary['allocations']} (`Box::new`, `Vec::new`, `String::from`, etc.)",
            f"- Total Memory Clones: {summary['clones']} (`.clone()` calls)",
            f"- Unsafe Scopes: {summary['unsafe_blocks']} `unsafe` blocks",
            f"- Borrows: {fn_info.borrow_count} reference instances\n",
            "=== CURRENT RUST QUALITY INDEX (RQI) EVALUATION ===",
            f"- Composite RQI Score: {rqi_summary.rqi_score:.2f} / 100 [{rqi_summary.grade}]",
            f"- Safety Vector: {rqi_summary.vectors.safety:.1f} / 100",
            f"- Performance Vector: {rqi_summary.vectors.performance:.1f} / 100",
            f"- Maintainability Vector: {rqi_summary.vectors.maintainability:.1f} / 100",
            f"- Security Vector: {rqi_summary.vectors.security:.1f} / 100\n",
        ]

        if all_deductions:
            prompt_lines.append("=== QUALITY DEDUCTIONS TO RESOLVE ===")
            for d in all_deductions:
                prompt_lines.append(f"- {d}")
            prompt_lines.append("")

        # Identified MITRE CWE Weakness Tags
        cwe_tags = rqi_summary.get_cwe_tags()
        if cwe_tags:
            prompt_lines.append("=== IDENTIFIED MITRE CWE WEAKNESS TAGS ===")
            for t in cwe_tags:
                loc = f" [Line {t['line_number']}]" if t.get('line_number') else ""
                stmt = f" -> `{t['statement_code']}`" if t.get('statement_code') else ""
                prompt_lines.append(f"- [{t['cwe_id']}{loc}] {t['name']} ({t['severity']}){stmt}")
                if t.get('remediation'):
                    prompt_lines.append(f"  Remediation: {t['remediation']}")
            prompt_lines.append("")

        if rqi_summary.penalty_applied:
            prompt_lines.append("=== NON-LINEAR PENALTIES ACTIVE ===")
            for p in rqi_summary.penalty_reasons:
                prompt_lines.append(f"- {p}")
            prompt_lines.append("")

        prompt_lines.append(
            "=== REFACTORING GOAL ==="
            "\nProduce an idiomatic, clean refactoring that resolves ALL quality deductions and CWE weaknesses above and scores near 100% RQI (A+ grade)."
            "\nDecompose the function into smaller helper functions where appropriate (e.g. separate formatting, logging, or complex checks) while preserving 100% of the original behavior."
            "\nEnsure the main refactored function keeps its original signature so callers are unaffected.\n\n"
            "=== REQUESTED ANALYSIS OUTPUT FORMAT ===\n"
            "Please structure your response into the following 3 markdown sections:\n\n"
            "### 1. Root Cause Explanation\n"
            "Provide a short overview sentence, followed by numbered items for each deduction in this format:\n"
            "1. **Defect Title ([CWE-ID if applicable])**:\n"
            "   - **Root Cause**: Specific explanation of the flaw, AST/FLOG graph invariant, or unsafe hazard.\n"
            "   - **Remediation**: Exact steps to fix it idiomatic to Rust.\n\n"
            "### 2. Proposed Idiomatic Refactored Patch\n"
            "```rust\n"
            "// Full standalone refactored code (main function + decomposed helper functions)\n"
            "```\n\n"
            "### 3. Estimated Optimization Metrics\n"
            "- Target Composite RQI: ~100 / 100 (A+ Idiomatic & Robust)\n"
            "- Safety Vector: 100 / 100 (Unsafe blocks & raw pointers removed)\n"
            "- Performance Vector: ~100 / 100 (Clones & redundant heap allocations eliminated)\n"
            "- Maintainability Vector: 100 / 100 (Decomposed into focused functions with V(G) <= 5)\n"
            "- Security Vector: 100 / 100 (Defensive boundary protected)"
        )

        return "\n".join(prompt_lines)


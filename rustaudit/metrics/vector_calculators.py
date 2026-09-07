"""
Quality Vector Calculator for RustAuditAI.
Evaluates 4 core analytical quality vectors: Safety, Performance, Maintainability, and Security.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from rustaudit.parser.rust_parser import FunctionAstInfo
from rustaudit.graph.cpg_builder import CodePropertyGraph


@dataclass
class VectorScores:
    safety: float
    performance: float
    maintainability: float
    security: float
    deductions: Dict[str, List[str]] = field(default_factory=dict)


class QualityVectorCalculator:
    """
    Computes mathematical quality vector scores (0-100) for a subroutine based on its CPG and AST attributes.
    """

    def calculate_vectors(self, fn_info: FunctionAstInfo, cpg: CodePropertyGraph) -> VectorScores:
        deductions: Dict[str, List[str]] = {
            "safety": [],
            "performance": [],
            "maintainability": [],
            "security": [],
        }

        # 1. Safety Vector Calculation
        safety_score = 100.0
        if fn_info.is_unsafe:
            safety_score -= 30.0
            deductions["safety"].append("Function marked with `unsafe` keyword (-30 pts)")

        if fn_info.unsafe_block_count > 0:
            penalty = fn_info.unsafe_block_count * 15.0
            safety_score -= penalty
            deductions["safety"].append(f"Contains {fn_info.unsafe_block_count} explicit `unsafe {{}}` block(s) (-{penalty} pts)")

        for stmt in fn_info.statements:
            if "as_ptr(" in stmt.code or "as_mut_ptr(" in stmt.code or "*" in stmt.code and "ptr" in stmt.code:
                safety_score -= 10.0
                deductions["safety"].append(f"Raw pointer operation detected in: `{stmt.code[:40]}...` (-10 pts)")

        safety_score = max(0.0, min(100.0, safety_score))

        # 2. Performance Vector Calculation
        performance_score = 100.0
        if fn_info.clone_count > 0:
            penalty = fn_info.clone_count * 15.0
            performance_score -= penalty
            deductions["performance"].append(f"Contains {fn_info.clone_count} `.clone()` call(s) causing memory copies (-{penalty} pts)")

        if fn_info.allocation_count > 0:
            penalty = fn_info.allocation_count * 10.0
            performance_score -= penalty
            deductions["performance"].append(f"Contains {fn_info.allocation_count} micro-heap allocation(s) (`Box::new`, `Vec::new`, etc.) (-{penalty} pts)")

        if fn_info.loop_count > 0 and fn_info.allocation_count > 0:
            performance_score -= 15.0
            deductions["performance"].append("Heap allocations performed inside loop structures (-15 pts)")

        performance_score = max(0.0, min(100.0, performance_score))

        # 3. Maintainability Vector Calculation
        maintainability_score = 100.0
        cc = cpg.cfg.graph.get("cyclomatic_complexity", 1)

        if cc > 10:
            penalty = (cc - 10) * 10.0 + 25.0
            maintainability_score -= penalty
            deductions["maintainability"].append(f"High McCabe Cyclomatic Complexity V(G)={cc} (>10 threshold) (-{penalty} pts)")
        elif cc > 5:
            penalty = (cc - 5) * 5.0
            maintainability_score -= penalty
            deductions["maintainability"].append(f"Moderate Cyclomatic Complexity V(G)={cc} (>5 threshold) (-{penalty} pts)")

        line_count = fn_info.line_end - fn_info.line_start + 1
        if line_count > 50:
            maintainability_score -= 20.0
            deductions["maintainability"].append(f"Subroutine length exceeds 50 lines ({line_count} lines) (-20 pts)")

        if len(fn_info.statements) > 12:
            maintainability_score -= 10.0
            deductions["maintainability"].append(f"High statement density ({len(fn_info.statements)} statements) (-10 pts)")

        maintainability_score = max(0.0, min(100.0, maintainability_score))

        # 4. Security Vector Calculation
        security_score = 100.0
        unwrap_count = sum(1 for stmt in fn_info.statements if ".unwrap(" in stmt.code or ".expect(" in stmt.code)

        if unwrap_count > 0:
            penalty = unwrap_count * 12.0
            security_score -= penalty
            deductions["security"].append(f"Unhandled `.unwrap()` / `.expect()` panic risks detected ({unwrap_count} instances) (-{penalty} pts)")

        unchecked_index = sum(1 for stmt in fn_info.statements if "[" in stmt.code and "]" in stmt.code and "get(" not in stmt.code)
        if unchecked_index > 0:
            security_score -= 10.0
            deductions["security"].append("Direct slice/array indexing without defensive `.get()` bounds checking (-10 pts)")

        if fn_info.is_unsafe or fn_info.unsafe_block_count > 0:
            security_score -= 15.0
            deductions["security"].append("Unsafe block exposes defensive security boundaries (-15 pts)")

        security_score = max(0.0, min(100.0, security_score))

        return VectorScores(
            safety=safety_score,
            performance=performance_score,
            maintainability=maintainability_score,
            security=security_score,
            deductions=deductions,
        )

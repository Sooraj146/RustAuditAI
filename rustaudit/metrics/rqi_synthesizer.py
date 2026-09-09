"""
Rust Quality Index (RQI) Synthesizer Engine for RustAuditAI.
Aggregates quality vector scores into a composite RQI score (0-100) using a dynamic non-linear penalty matrix.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from .vector_calculators import VectorScores, QualityVectorCalculator, VectorDeduction
from rustaudit.parser.rust_parser import FunctionAstInfo
from rustaudit.graph.cpg_builder import CodePropertyGraph


@dataclass
class RQISummary:
    function_name: str
    rqi_score: float
    grade: str
    vectors: VectorScores
    penalty_applied: bool
    penalty_reasons: List[str] = field(default_factory=list)

    @property
    def structured_deductions(self) -> Dict[str, List[VectorDeduction]]:
        return {
            "safety": [d for d in self.vectors.structured_deductions if d.vector == "safety"],
            "performance": [d for d in self.vectors.structured_deductions if d.vector == "performance"],
            "maintainability": [d for d in self.vectors.structured_deductions if d.vector == "maintainability"],
            "security": [d for d in self.vectors.structured_deductions if d.vector == "security"],
        }

    def get_cwe_tags(self) -> List[Dict[str, Any]]:
        tags = []
        seen = set()
        for d in self.vectors.structured_deductions:
            if d.cwe_id:
                key = (d.cwe_id, d.line_number)
                if key not in seen:
                    seen.add(key)
                    tags.append(d.to_dict())
        return tags

    def get_cwe_summary(self) -> Dict[str, Any]:
        counts = {"total": len(self.vectors.structured_deductions), "critical": 0, "high": 0, "medium": 0, "low": 0}
        for d in self.vectors.structured_deductions:
            sev = d.severity.lower()
            if sev in counts:
                counts[sev] += 1
            else:
                counts["medium"] += 1
        return counts

    def to_dict(self) -> Dict[str, Any]:
        return {
            "function_name": self.function_name,
            "rqi_score": round(self.rqi_score, 2),
            "grade": self.grade,
            "safety_score": round(self.vectors.safety, 2),
            "performance_score": round(self.vectors.performance, 2),
            "maintainability_score": round(self.vectors.maintainability, 2),
            "security_score": round(self.vectors.security, 2),
            "penalty_applied": self.penalty_applied,
            "penalty_reasons": self.penalty_reasons,
            "deductions": self.vectors.deductions,
            "structured_deductions": {
                k: [d.to_dict() for d in v]
                for k, v in self.structured_deductions.items()
            },
            "structured_deductions_list": [d.to_dict() for d in self.vectors.structured_deductions],
            "cwe_tags": self.get_cwe_tags(),
            "cwe_summary": self.get_cwe_summary(),
        }


class RQISynthesizer:
    """
    Synthesizes composite Rust Quality Index (RQI) scores.
    Formula:
    Base RQI = 0.30 * Safety + 0.25 * Performance + 0.25 * Maintainability + 0.20 * Security
    Applies non-linear penalties if critical vectors drop below threshold values.
    """

    WEIGHT_SAFETY = 0.30
    WEIGHT_PERFORMANCE = 0.25
    WEIGHT_MAINTAINABILITY = 0.25
    WEIGHT_SECURITY = 0.20

    def __init__(self):
        self.calculator = QualityVectorCalculator()

    def compute_rqi(self, fn_info: FunctionAstInfo, cpg: CodePropertyGraph) -> RQISummary:
        vectors = self.calculator.calculate_vectors(fn_info, cpg)

        base_rqi = (
            self.WEIGHT_SAFETY * vectors.safety
            + self.WEIGHT_PERFORMANCE * vectors.performance
            + self.WEIGHT_MAINTAINABILITY * vectors.maintainability
            + self.WEIGHT_SECURITY * vectors.security
        )

        penalty_applied = False
        penalty_reasons = []

        # Non-linear penalty matrix: Safety < 60 triggers cross-vector 15% penalty
        if vectors.safety < 60.0:
            base_rqi *= 0.85
            penalty_applied = True
            penalty_reasons.append("Critical Safety penalty applied (Safety < 60 triggers 15% cross-vector deduction)")

        # Performance < 50 triggers 10% penalty
        if vectors.performance < 50.0:
            base_rqi *= 0.90
            penalty_applied = True
            penalty_reasons.append("Performance bottleneck penalty applied (Performance < 50 triggers 10% deduction)")

        final_rqi = max(0.0, min(100.0, base_rqi))

        # Assign letter grade based on RQI score
        if final_rqi >= 90.0:
            grade = "A+ (Idiomatic & Robust)"
        elif final_rqi >= 80.0:
            grade = "A (Good Quality)"
        elif final_rqi >= 70.0:
            grade = "B (Acceptable)"
        elif final_rqi >= 60.0:
            grade = "C (Needs Refactoring)"
        elif final_rqi >= 50.0:
            grade = "D (High Risk / Inefficient)"
        else:
            grade = "F (Critical Vulnerability / Inefficient)"

        return RQISummary(
            function_name=fn_info.name,
            rqi_score=final_rqi,
            grade=grade,
            vectors=vectors,
            penalty_applied=penalty_applied,
            penalty_reasons=penalty_reasons,
        )

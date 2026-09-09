"""
Unit and API integration tests for RustAuditAI Reporting & Export Engine (SRS §4.6.5).
Validates publication-grade PDF generation and machine-readable JSON exports.
"""

import io
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from rustaudit.reports.pdf_generator import RustAuditPDFReportGenerator, generate_pdf_report
from rustaudit.server import app

client = TestClient(app)


def test_pdf_report_generation_clean_code():
    """Validates PDF generation for clean functions without defects."""
    generator = RustAuditPDFReportGenerator()
    data = {
        "name": "safe_calculate",
        "visibility": "pub",
        "is_unsafe": False,
        "is_async": False,
        "line_start": 1,
        "line_end": 8,
        "metrics": {
            "clone_count": 0,
            "allocation_count": 0,
            "unsafe_block_count": 0,
            "borrow_count": 2,
            "loop_count": 0,
            "branch_count": 1,
        },
        "cpg_summary": {
            "ast_nodes": 18,
            "ast_edges": 17,
            "cfg_nodes": 4,
            "cfg_edges": 4,
            "cyclomatic_complexity": 2,
            "flog_nodes": 3,
            "flog_edges": 2,
            "cpg_nodes": 25,
            "cpg_edges": 27,
        },
        "rqi": {
            "rqi_score": 96.5,
            "grade": "A+ (Idiomatic & Robust)",
            "safety_score": 100.0,
            "performance_score": 95.0,
            "maintainability_score": 95.0,
            "security_score": 96.0,
            "penalty_applied": False,
            "penalty_reasons": [],
            "structured_deductions_list": [],
        },
        "cwe_summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
        "cwe_tags": [],
    }

    pdf_bytes = generator.generate(data, filename="safe_calc.rs")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 2000


def test_pdf_report_generation_with_deductions():
    """Validates PDF generation for code with multiple CWE defects, penalties, and remediation guidance."""
    data = {
        "name": "vulnerable_buffer_copy",
        "visibility": "pub",
        "is_unsafe": True,
        "is_async": False,
        "line_start": 10,
        "line_end": 45,
        "metrics": {
            "clone_count": 5,
            "allocation_count": 8,
            "unsafe_block_count": 2,
            "borrow_count": 4,
            "loop_count": 2,
            "branch_count": 4,
        },
        "cpg_summary": {
            "ast_nodes": 78,
            "ast_edges": 82,
            "cfg_nodes": 24,
            "cfg_edges": 30,
            "cyclomatic_complexity": 5,
            "flog_nodes": 15,
            "flog_edges": 18,
            "cpg_nodes": 110,
            "cpg_edges": 135,
        },
        "rqi": {
            "rqi_score": 52.3,
            "grade": "D (Unsafe / Deficient)",
            "safety_score": 45.0,
            "performance_score": 55.0,
            "maintainability_score": 60.0,
            "security_score": 50.0,
            "penalty_applied": True,
            "penalty_reasons": [
                "Critical Safety penalty applied (Safety < 60 triggers 15% cross-vector deduction)"
            ],
            "structured_deductions_list": [
                {
                    "cwe_id": "CWE-119",
                    "cwe_name": "Improper Restriction of Operations within Bounds of Memory Buffer",
                    "severity": "CRITICAL",
                    "penalty": 20.0,
                    "message": "Raw pointer offset dereference without bound checks in unsafe block.",
                    "line_number": 22,
                    "statement_code": "*ptr.offset(i as isize) = val;",
                    "remediation": "Replace raw pointer manipulation with bounds-checked slice indexing or iterators.",
                    "vector": "safety",
                },
                {
                    "cwe_id": "CWE-401",
                    "cwe_name": "Missing Release of Memory after Effective Lifetime (Memory Leak)",
                    "severity": "HIGH",
                    "penalty": 15.0,
                    "message": "Excessive redundant clones inside inner loop body.",
                    "line_number": 31,
                    "statement_code": "let copy = buffer.clone();",
                    "remediation": "Borrow slice (&[u8]) or utilize Rc/Arc for shared ownership without deep copying.",
                    "vector": "performance",
                },
            ],
        },
        "cwe_summary": {"total": 2, "critical": 1, "high": 1, "medium": 0, "low": 0},
        "cwe_tags": [
            {"cwe_id": "CWE-119", "severity": "CRITICAL", "line_number": 22},
            {"cwe_id": "CWE-401", "severity": "HIGH", "line_number": 31},
        ],
    }

    pdf_bytes = generate_pdf_report(data, filename="vuln_copy.rs")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 4000


def test_pdf_report_with_xai():
    """Validates PDF generation including Explainable AI diagnosis and refactored patch candidate."""
    data = {
        "name": "process_items",
        "visibility": "pub",
        "is_unsafe": False,
        "line_start": 1,
        "line_end": 15,
        "metrics": {"clone_count": 2, "allocation_count": 3, "unsafe_block_count": 0, "borrow_count": 1, "loop_count": 1, "branch_count": 1},
        "cpg_summary": {"ast_nodes": 30, "ast_edges": 29, "cfg_nodes": 6, "cfg_edges": 7, "cyclomatic_complexity": 2, "flog_nodes": 5, "flog_edges": 4, "cpg_nodes": 40, "cpg_edges": 42},
        "rqi": {
            "rqi_score": 75.0,
            "grade": "B (Good)",
            "safety_score": 85.0,
            "performance_score": 70.0,
            "maintainability_score": 75.0,
            "security_score": 70.0,
            "penalty_applied": False,
            "penalty_reasons": [],
            "structured_deductions_list": [],
        },
        "cwe_summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
        "cwe_tags": [],
        "xai_report": {
            "explanation": "Memory duplication identified: unnecessary `.clone()` calls inside loop condition can be avoided using iterators.",
            "refactored_code": "pub fn process_items(items: &[String]) -> usize {\n    items.iter().filter(|s| !s.is_empty()).count()\n}",
        },
    }

    pdf_bytes = generate_pdf_report(data, filename="items.rs")
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 3000


def test_pdf_report_multi_function():
    """Validates PDF generation for multi-function payloads producing portfolio tables."""
    multi_data = {
        "filename": "multi_module.rs",
        "functions": [
            {
                "name": "func_a",
                "visibility": "pub",
                "is_unsafe": False,
                "line_start": 1,
                "line_end": 10,
                "metrics": {"clone_count": 0, "allocation_count": 0, "unsafe_block_count": 0, "borrow_count": 1, "loop_count": 0, "branch_count": 1},
                "cpg_summary": {"ast_nodes": 12, "ast_edges": 11, "cfg_nodes": 3, "cfg_edges": 3, "cyclomatic_complexity": 1, "flog_nodes": 2, "flog_edges": 1, "cpg_nodes": 15, "cpg_edges": 15},
                "rqi": {"rqi_score": 92.0, "grade": "Grade A", "safety_score": 95.0, "performance_score": 90.0, "maintainability_score": 90.0, "security_score": 95.0, "penalty_applied": False, "penalty_reasons": [], "structured_deductions_list": []},
                "cwe_summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
                "cwe_tags": [],
            },
            {
                "name": "func_b",
                "visibility": "pub",
                "is_unsafe": True,
                "line_start": 12,
                "line_end": 30,
                "metrics": {"clone_count": 1, "allocation_count": 2, "unsafe_block_count": 1, "borrow_count": 1, "loop_count": 1, "branch_count": 2},
                "cpg_summary": {"ast_nodes": 25, "ast_edges": 24, "cfg_nodes": 8, "cfg_edges": 9, "cyclomatic_complexity": 3, "flog_nodes": 4, "flog_edges": 4, "cpg_nodes": 35, "cpg_edges": 38},
                "rqi": {"rqi_score": 70.0, "grade": "Grade B", "safety_score": 65.0, "performance_score": 75.0, "maintainability_score": 70.0, "security_score": 70.0, "penalty_applied": False, "penalty_reasons": [], "structured_deductions_list": []},
                "cwe_summary": {"total": 1, "critical": 0, "high": 1, "medium": 0, "low": 0},
                "cwe_tags": [{"cwe_id": "CWE-401", "severity": "HIGH", "line_number": 18}],
            },
        ],
    }

    pdf_bytes = generate_pdf_report(multi_data, filename="multi_module.rs")
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 5000


def test_api_export_pdf_endpoint():
    """Validates POST /api/export/pdf endpoint with standard response headers."""
    payload = {
        "function_data": {
            "name": "compute_hash",
            "visibility": "pub",
            "is_unsafe": False,
            "line_start": 1,
            "line_end": 15,
            "metrics": {"clone_count": 0, "allocation_count": 1, "unsafe_block_count": 0, "borrow_count": 1, "loop_count": 0, "branch_count": 0},
            "cpg_summary": {"ast_nodes": 14, "ast_edges": 13, "cfg_nodes": 3, "cfg_edges": 3, "cyclomatic_complexity": 1, "flog_nodes": 2, "flog_edges": 1, "cpg_nodes": 18, "cpg_edges": 19},
            "rqi": {
                "rqi_score": 90.0,
                "grade": "Grade A",
                "safety_score": 95.0,
                "performance_score": 90.0,
                "maintainability_score": 85.0,
                "security_score": 90.0,
                "penalty_applied": False,
                "penalty_reasons": [],
                "structured_deductions_list": [],
            },
            "cwe_summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
            "cwe_tags": [],
        },
        "filename": "hasher.rs",
    }

    resp = client.post("/api/export/pdf", json=payload)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in resp.headers["content-disposition"]
    assert "rustaudit_report_compute_hash.pdf" in resp.headers["content-disposition"]
    assert resp.content.startswith(b"%PDF-")
    assert len(resp.content) > 2000



def test_api_export_errors():
    """Validates error response when audit data is missing."""
    resp = client.post("/api/export/pdf", json={})
    assert resp.status_code == 400

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.cwe import CWERegistry, CWETag
from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder, GraphOutlierAnalyzer
from rustaudit.metrics import RQISynthesizer
from fastapi.testclient import TestClient
from rustaudit.server import app


def test_cwe_registry():
    """Verify CWE catalog contains required definitions and produces valid tags."""
    registry = CWERegistry()
    
    # Check required core CWEs exist
    required_cwes = [
        "CWE-119", "CWE-476", "CWE-416", "CWE-252",
        "CWE-129", "CWE-400", "CWE-770", "CWE-710",
        "CWE-1075", "CWE-676", "CWE-703"
    ]
    for cwe_id in required_cwes:
        defn = registry.get(cwe_id)
        assert defn is not None, f"Missing definition for {cwe_id}"
        assert defn.cwe_id == cwe_id
        assert defn.url == f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html"
        assert defn.default_severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        assert len(defn.remediation) > 10

    # Test tagging by detection key
    tag_unsafe = registry.tag_from_detection("unsafe_operation", line_number=15, statement_code="unsafe { *ptr }")
    assert tag_unsafe.cwe_id == "CWE-119"
    assert tag_unsafe.severity == "HIGH"
    assert tag_unsafe.line_number == 15
    assert tag_unsafe.statement_code == "unsafe { *ptr }"
    assert "https://cwe.mitre.org" in tag_unsafe.url

    # Test severity override
    tag_crit = registry.tag_from_detection("unsafe_operation", severity_override="CRITICAL")
    assert tag_crit.severity == "CRITICAL"

    tag_clone = registry.tag_from_detection("clone_in_loop", line_number=22)
    assert tag_clone.cwe_id == "CWE-400"
    assert tag_clone.severity == "MEDIUM"
    assert tag_clone.line_number == 22


def test_statement_line_resolution():
    """Verify statement-level 1-based source line numbers are computed."""
    parser = RustParser()
    code = """
pub fn example(data: &str) -> String {
    let mut s = String::from(data);
    let copy = s.clone();
    unsafe {
        let raw = copy.as_ptr();
    }
    s
}
"""
    res = parser.parse_code(code)
    assert res.success is True
    assert len(res.functions) == 1
    fn = res.functions[0]
    
    # Every statement must have a valid positive 1-based line number
    for stmt in fn.statements:
        assert stmt.line_number is not None, f"Statement '{stmt.code}' missing line number"
        assert fn.line_start <= stmt.line_number <= fn.line_end, (
            f"Line {stmt.line_number} outside function [{fn.line_start}, {fn.line_end}]"
        )


def test_outlier_cwe_tagging():
    """Verify GraphOutlierAnalyzer associates CWE metadata with graph anomalies."""
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"
    res = parser.parse_file(str(sample_path))
    assert res.success is True

    fn1 = res.functions[0]
    builder = CPGBuilder()
    cpg1 = builder.build_cpg(fn1)
    analyzer = GraphOutlierAnalyzer()
    report1 = analyzer.analyze_outliers(fn1, cpg1)

    cwe_tags = report1.get_cwe_tags()
    assert len(cwe_tags) > 0, "Expected CWE tags from outlier analyzer"

    for tag in cwe_tags:
        assert tag["cwe_id"].startswith("CWE-")
        assert tag["severity"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        assert tag["url"].startswith("https://cwe.mitre.org")
        assert len(tag["remediation"]) > 0


def test_rqi_structured_deductions_cwe():
    """Verify RQISynthesizer generates structured deductions with CWE tags and summary."""
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"
    res = parser.parse_file(str(sample_path))
    assert res.success is True

    fn1 = res.functions[0]
    builder = CPGBuilder()
    cpg1 = builder.build_cpg(fn1)
    synthesizer = RQISynthesizer()
    rqi1 = synthesizer.compute_rqi(fn1, cpg1)

    # Check structured deductions
    has_structured = False
    for vec, deductions in rqi1.structured_deductions.items():
        if deductions:
            has_structured = True
            for d in deductions:
                assert d.severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
                if d.cwe_id:
                    assert d.cwe_id.startswith("CWE-")
                    assert d.cwe_url.startswith("https://cwe.mitre.org")
                if d.remediation:
                    assert len(d.remediation) > 0

    assert has_structured, "Expected structured deductions in RQI summary"

    # Check CWE summary
    summary = rqi1.get_cwe_summary()
    assert "total" in summary
    assert "critical" in summary
    assert "high" in summary
    assert "medium" in summary
    assert "low" in summary
    assert summary["total"] >= 1
    assert summary["total"] == summary["critical"] + summary["high"] + summary["medium"] + summary["low"]

    # Check to_dict serialization
    rqi_dict = rqi1.to_dict()
    assert "structured_deductions" in rqi_dict
    assert "cwe_tags" in rqi_dict
    assert "cwe_summary" in rqi_dict


def test_api_analyze_cwe_payload():
    """Verify /api/analyze returns CWE tags and summary in API response."""
    client = TestClient(app)
    code = """
pub fn test_fn(x: &str) -> String {
    let mut s = String::from(x);
    let c = s.clone();
    unsafe {
        let p = c.as_ptr();
    }
    s
}
"""
    response = client.post("/api/analyze", json={"code": code, "explain": False})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "overall_cwe_summary" in data
    assert data["overall_cwe_summary"]["total"] >= 1

    fn = data["functions"][0]
    assert "cwe_tags" in fn
    assert "cwe_summary" in fn
    assert fn["cwe_summary"]["total"] >= 1
    assert len(fn["cwe_tags"]) >= 1

    tag = fn["cwe_tags"][0]
    assert tag["cwe_id"].startswith("CWE-")
    assert tag["url"].startswith("https://cwe.mitre.org")
    assert tag["severity"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")


if __name__ == "__main__":
    test_cwe_registry()
    test_statement_line_resolution()
    test_outlier_cwe_tagging()
    test_rqi_structured_deductions_cwe()
    test_api_analyze_cwe_payload()
    print("\n[OK] All CWE Identification Tagging tests passed successfully!")

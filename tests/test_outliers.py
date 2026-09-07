import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder, GraphOutlierAnalyzer


def test_outlier_analyzer():
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"

    res = parser.parse_file(str(sample_path))
    assert res.success is True
    assert len(res.functions) > 0

    builder = CPGBuilder()
    analyzer = GraphOutlierAnalyzer()

    # Function 1: process_user_data
    fn1 = res.functions[0]
    cpg1 = builder.build_cpg(fn1)
    report1 = analyzer.analyze_outliers(fn1, cpg1)

    print("[OK] Graph Outliers Analyzed for:", fn1.name)
    print("   - AST Outliers:", len(report1.ast_outliers))
    print("   - CFG Outliers:", len(report1.cfg_outliers))
    print("   - FLOG Outliers:", len(report1.flog_outliers))

    assert len(report1.flog_outliers) >= 1  # Should flag clone & unsafe operations in FLOG

    for o in report1.flog_outliers:
        print(f"     * [{o.severity}] {o.title}: {o.description}")

    print("\n[OK] All Outlier Analyzer tests passed successfully!")


if __name__ == "__main__":
    test_outlier_analyzer()

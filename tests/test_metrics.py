import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder
from rustaudit.metrics import RQISynthesizer


def test_rqi_metrics():
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"

    res = parser.parse_file(str(sample_path))
    assert res.success is True
    assert len(res.functions) == 2

    builder = CPGBuilder()
    synthesizer = RQISynthesizer()

    # Function 1: process_user_data (contains unsafe, clone, allocations)
    fn1 = res.functions[0]
    cpg1 = builder.build_cpg(fn1)
    rqi1 = synthesizer.compute_rqi(fn1, cpg1)

    print("[OK] RQI Calculated for:", fn1.name)
    print(f"   - RQI Score: {rqi1.rqi_score:.2f} / 100 ({rqi1.grade})")
    print(f"   - Safety: {rqi1.vectors.safety:.2f}")
    print(f"   - Performance: {rqi1.vectors.performance:.2f}")
    print(f"   - Maintainability: {rqi1.vectors.maintainability:.2f}")
    print(f"   - Security: {rqi1.vectors.security:.2f}")
    print(f"   - Penalty Applied: {rqi1.penalty_applied}")

    assert 0.0 <= rqi1.rqi_score <= 100.0
    assert rqi1.vectors.safety < 100.0  # due to unsafe block
    assert rqi1.vectors.performance < 100.0  # due to clone & Box::new

    # Function 2: calculate_metrics (clean idiomatic loop function)
    fn2 = res.functions[1]
    cpg2 = builder.build_cpg(fn2)
    rqi2 = synthesizer.compute_rqi(fn2, cpg2)

    print("\n[OK] RQI Calculated for:", fn2.name)
    print(f"   - RQI Score: {rqi2.rqi_score:.2f} / 100 ({rqi2.grade})")
    print(f"   - Safety: {rqi2.vectors.safety:.2f}")
    print(f"   - Performance: {rqi2.vectors.performance:.2f}")
    print(f"   - Maintainability: {rqi2.vectors.maintainability:.2f}")
    print(f"   - Security: {rqi2.vectors.security:.2f}")

    assert rqi2.rqi_score > rqi1.rqi_score  # Clean function scores higher than unsafe/cloning function

    print("\n[OK] All Phase 3 RQI Metric Engine tests passed successfully!")


if __name__ == "__main__":
    test_rqi_metrics()

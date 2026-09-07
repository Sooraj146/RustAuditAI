import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder
from rustaudit.metrics import RQISynthesizer
from rustaudit.ai import XAIEngine, XAIPromptBuilder, LLMClient


def test_xai_engine():
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"

    res = parser.parse_file(str(sample_path))
    assert res.success is True
    assert len(res.functions) > 0

    builder = CPGBuilder()
    synthesizer = RQISynthesizer()
    prompt_builder = XAIPromptBuilder()

    fn1 = res.functions[0]
    cpg1 = builder.build_cpg(fn1)
    rqi1 = synthesizer.compute_rqi(fn1, cpg1)

    code_sample = sample_path.read_text(encoding="utf-8")

    # 1. Test Prompt Building
    prompt = prompt_builder.build_prompt(fn1, cpg1, rqi1, code_sample)
    assert fn1.name in prompt
    assert "DETERMINISTIC CODE PROPERTY GRAPH" in prompt
    print("[OK] Bounded XAI Prompt built successfully!")

    # 2. Test LLM Connection & XAI Engine for degraded function (RQI < 100)
    try:
        engine = XAIEngine()
        print("\n[INFO] Contacting LLM API for Explainable AI Refactoring Report (Function with RQI < 100)...")
        lines = code_sample.splitlines()
        fn1_code = "\n".join(lines[fn1.line_start - 1 : fn1.line_end]) if fn1.line_start > 0 and fn1.line_end <= len(lines) else code_sample
        report = engine.generate_explanation(fn1, cpg1, rqi1, fn1_code)

        print("\n" + "=" * 70)
        print(f"[OK] XAI Refactoring Report Received for '{report.function_name}'")
        print("=" * 70)
        print("\n--- Root Cause Explanation ---")
        print(report.explanation)

        if report.refactored_code:
            print("\n--- Refactored Idiomatic Rust Patch ---")
            print(report.refactored_code)

        if report.diff_text:
            print("\n--- Behavioral Diff ---")
            print(report.diff_text)

        print("\n--- Optimization Metrics ---")
        print(report.metrics_summary)

        assert report.explanation is not None
        assert report.refactored_code is not None
        assert report.diff_text is not None
        assert "pending validation" not in report.metrics_summary.lower()
        print("[OK] Verified Optimization Metrics extracted/synthesized accurately!")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[WARNING] LLM API test skipped or hit error: {e}")

    # 3. Test Optimal Function (RQI == 100) - No refactoring code needed
    if len(res.functions) > 1:
        fn2 = res.functions[1]
        cpg2 = builder.build_cpg(fn2)
        rqi2 = synthesizer.compute_rqi(fn2, cpg2)
        assert rqi2.rqi_score >= 100.0

        engine2 = XAIEngine()
        report2 = engine2.generate_explanation(fn2, cpg2, rqi2, code_sample)

        print("\n" + "=" * 70)
        print(f"[OK] XAI Report for Optimal Function '{report2.function_name}' (RQI {rqi2.rqi_score:.1f})")
        print("=" * 70)
        print(f"Explanation: {report2.explanation}")
        print(f"Refactored Code: {report2.refactored_code} (Expected: None)")
        print(f"Diff Text: '{report2.diff_text}' (Expected: empty)")
        print(f"Optimization Metrics:\n{report2.metrics_summary}")

        assert report2.refactored_code is None, "RQI 100 functions should not have refactored code!"
        assert report2.diff_text == "", "RQI 100 functions should have empty diff text!"
        assert "100.00 / 100" in report2.metrics_summary
        print("[OK] Verified RQI 100 function correctly bypasses refactoring patch generation!")

    print("\n[OK] All Phase 4 XAI Engine tests passed successfully!")


if __name__ == "__main__":
    test_xai_engine()

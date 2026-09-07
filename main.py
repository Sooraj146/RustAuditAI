import sys
import json
from pathlib import Path
from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder
from rustaudit.metrics import RQISynthesizer
from rustaudit.ai import XAIEngine


def main():
    if len(sys.argv) < 2:
        print("RustAuditAI - Intra-Procedural Quality Assessment System")
        print("Usage: python main.py <path_to_rust_file.rs> [--explain]")
        sys.exit(1)

    file_path = sys.argv[1]
    enable_ai = "--explain" in sys.argv or "--ai" in sys.argv

    parser = RustParser()
    builder = CPGBuilder()
    synthesizer = RQISynthesizer()
    ai_engine = XAIEngine() if enable_ai else None

    result = parser.parse_file(file_path)

    if not result.success:
        print(f"[ERROR] Failed to parse {file_path}: {result.error}")
        sys.exit(1)

    code_content = Path(file_path).read_text(encoding="utf-8")

    print("=" * 70)
    print(f"RustAuditAI Assessment Report for: {file_path}")
    print("=" * 70)
    print(f"Total Functions Analyzed: {len(result.functions)}\n")

    for idx, fn in enumerate(result.functions, start=1):
        cpg = builder.build_cpg(fn)
        rqi_summary = synthesizer.compute_rqi(fn, cpg)

        print(f"[{idx}] Function: '{fn.name}' ({fn.visibility}) | Lines {fn.line_start}-{fn.line_end}")
        print(f"    [RQI SCORE]: {rqi_summary.rqi_score:.2f} / 100 [{rqi_summary.grade}]")
        print(f"    [VECTORS]: Safety={rqi_summary.vectors.safety:.1f} | Perf={rqi_summary.vectors.performance:.1f} | Maint={rqi_summary.vectors.maintainability:.1f} | Sec={rqi_summary.vectors.security:.1f}")

        if rqi_summary.penalty_applied:
            print("    [NON-LINEAR PENALTIES]:")
            for reason in rqi_summary.penalty_reasons:
                print(f"       - {reason}")

        all_deductions = [d for sublist in rqi_summary.vectors.deductions.values() for d in sublist]
        if all_deductions:
            print("    [DETAILED DEDUCTIONS]:")
            for d in all_deductions:
                print(f"       * {d}")

        if ai_engine:
            print("\n    [EXPLAINABLE AI REFACTORING REPORT]:")
            try:
                lines = code_content.splitlines()
                if fn.line_start > 0 and fn.line_end <= len(lines):
                    fn_code = "\n".join(lines[fn.line_start - 1 : fn.line_end])
                else:
                    fn_code = code_content

                report = ai_engine.generate_explanation(fn, cpg, rqi_summary, fn_code)
                print(f"\n    --- Explanation ---\n    {report.explanation.replace(chr(10), chr(10) + '    ')}")
                if report.refactored_code:
                    print(f"\n    --- Idiomatic Patch ---\n    {report.refactored_code.replace(chr(10), chr(10) + '    ')}")
            except Exception as e:
                print(f"    [WARNING] Could not generate AI report: {e}")

        print("-" * 70)


if __name__ == "__main__":
    main()


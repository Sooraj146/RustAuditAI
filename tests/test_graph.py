import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder


def test_graph_builder():
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"

    res = parser.parse_file(str(sample_path))
    assert res.success is True
    assert len(res.functions) == 2

    builder = CPGBuilder()

    # Test Function 1: process_user_data
    cpg1 = builder.build_cpg(res.functions[0])
    summary1 = cpg1.summary()

    print("[OK] CPG 1 Built for function:", summary1["function_name"])
    print(f"   - AST: {summary1['ast_nodes']} nodes, {summary1['ast_edges']} edges")
    print(f"   - CFG: {summary1['cfg_nodes']} nodes, {summary1['cfg_edges']} edges | Cyclomatic Complexity: {summary1['cyclomatic_complexity']}")
    print(f"   - FLOG: {summary1['flog_nodes']} nodes, {summary1['flog_edges']} edges | Clones: {summary1['clones']}, Allocations: {summary1['allocations']}, Unsafe: {summary1['unsafe_blocks']}")
    print(f"   - Unified CPG: {summary1['cpg_nodes']} nodes, {summary1['cpg_edges']} edges")

    assert summary1["ast_nodes"] > 0
    assert summary1["cfg_nodes"] > 0
    assert summary1["flog_nodes"] > 0
    assert summary1["cyclomatic_complexity"] >= 2
    assert summary1["clones"] == 1
    assert summary1["allocations"] >= 1
    assert summary1["unsafe_blocks"] == 1

    # Test Function 2: calculate_metrics
    cpg2 = builder.build_cpg(res.functions[1])
    summary2 = cpg2.summary()

    print("\n[OK] CPG 2 Built for function:", summary2["function_name"])
    print(f"   - AST: {summary2['ast_nodes']} nodes, {summary2['ast_edges']} edges")
    print(f"   - CFG: {summary2['cfg_nodes']} nodes, {summary2['cfg_edges']} edges | Cyclomatic Complexity: {summary2['cyclomatic_complexity']}")
    print(f"   - FLOG: {summary2['flog_nodes']} nodes, {summary2['flog_edges']} edges | Clones: {summary2['clones']}, Allocations: {summary2['allocations']}")
    print(f"   - Unified CPG: {summary2['cpg_nodes']} nodes, {summary2['cpg_edges']} edges")

    assert summary2["cyclomatic_complexity"] >= 2

    print("\n[OK] All Phase 2 Graph Abstraction tests passed successfully!")


if __name__ == "__main__":
    test_graph_builder()

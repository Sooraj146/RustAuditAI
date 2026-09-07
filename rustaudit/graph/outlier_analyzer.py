"""
Graph Outlier Analyzer Engine for RustAuditAI.
Analyzes AST, CFG, and FLOG graph topologies to extract domain-specific outliers, anomalies, and structural hotspots.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from rustaudit.parser.rust_parser import FunctionAstInfo
from .cpg_builder import CodePropertyGraph


@dataclass
class GraphOutlierItem:
    graph_type: str  # "AST", "CFG", or "FLOG"
    severity: str    # "HIGH", "MEDIUM", "INFO"
    title: str
    description: str
    affected_nodes: List[str] = field(default_factory=list)


@dataclass
class GraphOutliersReport:
    ast_outliers: List[GraphOutlierItem] = field(default_factory=list)
    cfg_outliers: List[GraphOutlierItem] = field(default_factory=list)
    flog_outliers: List[GraphOutlierItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ast": [item.__dict__ for item in self.ast_outliers],
            "cfg": [item.__dict__ for item in self.cfg_outliers],
            "flog": [item.__dict__ for item in self.flog_outliers],
        }


class GraphOutlierAnalyzer:
    """
    Identifies structural and semantic outliers across Abstract Syntax Trees, Control Flow Graphs, and Function-Level Ownership Graphs.
    """

    def analyze_outliers(self, fn_info: FunctionAstInfo, cpg: CodePropertyGraph) -> GraphOutliersReport:
        ast_outliers: List[GraphOutlierItem] = []
        cfg_outliers: List[GraphOutlierItem] = []
        flog_outliers: List[GraphOutlierItem] = []

        # --- 1. AST Graph Outliers ---
        if fn_info.is_unsafe:
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="HIGH",
                    title="Unsafe Function Scope Signature",
                    description=f"Function `{fn_info.name}` is declared with the `unsafe` keyword, bypassing rustc compile-time invariants for its entire body.",
                    affected_nodes=[f"fn_{fn_info.name}"],
                )
            )

        if len(fn_info.inputs) > 3:
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="MEDIUM",
                    title="High Parameter Count Anomaly",
                    description=f"Function accepts {len(fn_info.inputs)} parameters. Consider grouping related parameters into a dedicated struct to improve maintainability.",
                    affected_nodes=[f"fn_{fn_info.name}_params"],
                )
            )

        if len(fn_info.statements) > 10:
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="INFO",
                    title="High AST Statement Density",
                    description=f"AST contains {len(fn_info.statements)} statements in a single subroutine block.",
                    affected_nodes=[f"fn_{fn_info.name}_body"],
                )
            )

        # --- 2. CFG Graph Outliers ---
        cc = cpg.cfg.graph.get("cyclomatic_complexity", 1)
        if cc > 5:
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="HIGH" if cc > 10 else "MEDIUM",
                    title=f"Cyclomatic Complexity Hotspot (V(G) = {cc})",
                    description=f"Control Flow Graph exhibits elevated branching complexity ({cc} independent execution paths). High risk of unhandled condition branches.",
                    affected_nodes=[n for n, d in cpg.cfg.nodes(data=True) if d.get("is_decision")],
                )
            )

        decision_nodes = [n for n, d in cpg.cfg.nodes(data=True) if d.get("is_decision")]
        if decision_nodes:
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="INFO",
                    title="Conditional Branch Divergence Nodes",
                    description=f"Identified {len(decision_nodes)} branching decision points splitting control flow execution paths.",
                    affected_nodes=decision_nodes,
                )
            )

        loop_nodes = [n for n, d in cpg.cfg.nodes(data=True) if d.get("is_loop")]
        if loop_nodes:
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="MEDIUM",
                    title="Cyclic Control Loop Back-Edge",
                    description=f"CFG contains {len(loop_nodes)} loop header latch node(s) introducing cyclic control flow edges.",
                    affected_nodes=loop_nodes,
                )
            )

        # --- 3. FLOG Ownership Graph Outliers ---
        if fn_info.clone_count > 0:
            clone_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("is_clone")]
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="HIGH",
                    title="Deep Memory Copy (.clone()) Hotspot",
                    description=f"FLOG detected {fn_info.clone_count} explicit `.clone()` mutation node(s). High memory bandwidth overhead.",
                    affected_nodes=clone_nodes,
                )
            )

        if fn_info.allocation_count > 0:
            alloc_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("is_heap_alloc")]
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="MEDIUM",
                    title="Micro-Heap Allocation Binding",
                    description=f"FLOG mapped {fn_info.allocation_count} heap allocation node(s) (`Box::new`, `Vec::new`, `String::from`).",
                    affected_nodes=alloc_nodes,
                )
            )

        if fn_info.unsafe_block_count > 0:
            unsafe_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("node_type") == "UnsafeOperation"]
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="HIGH",
                    title="Unsafe Memory Lifecycle Scope",
                    description=f"FLOG maps {fn_info.unsafe_block_count} explicit unsafe block node(s) where lifetime & borrow safety checks are suspended.",
                    affected_nodes=unsafe_nodes,
                )
            )

        return GraphOutliersReport(
            ast_outliers=ast_outliers,
            cfg_outliers=cfg_outliers,
            flog_outliers=flog_outliers,
        )

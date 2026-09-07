"""
Control Flow Graph (CFG) Builder for RustAuditAI.
Constructs basic blocks, control flow edges, and calculates McCabe's Cyclomatic Complexity.
"""

from typing import Dict, List, Tuple
import networkx as nx
from rustaudit.parser.rust_parser import FunctionAstInfo, StatementSummary


class CFGGraphBuilder:
    """
    Constructs an intra-procedural Control Flow Graph (CFG) for a Rust function.
    """

    def build_cfg_graph(self, fn_info: FunctionAstInfo) -> nx.DiGraph:
        cfg = nx.DiGraph()

        entry_node = f"cfg_{fn_info.name}_ENTRY"
        exit_node = f"cfg_{fn_info.name}_EXIT"

        cfg.add_node(entry_node, node_type="ENTRY", label="ENTRY")
        cfg.add_node(exit_node, node_type="EXIT", label="EXIT")

        if not fn_info.statements:
            cfg.add_edge(entry_node, exit_node, edge_type="FLOW")
            cfg.graph["cyclomatic_complexity"] = 1
            return cfg

        prev_node = entry_node
        branch_count = fn_info.branch_count
        loop_count = fn_info.loop_count

        # Build basic blocks or statement nodes connected in control order
        for idx, stmt in enumerate(fn_info.statements):
            curr_node = f"cfg_{fn_info.name}_block_{idx}"

            is_decision_pt = ("Expr(If)" in stmt.kind or "Expr(Match)" in stmt.kind or "if " in stmt.code or "match " in stmt.code)
            is_loop_pt = ("Expr(Loop)" in stmt.kind or "loop" in stmt.code or "for " in stmt.code or "while " in stmt.code)

            cfg.add_node(
                curr_node,
                node_type="DecisionBlock" if is_decision_pt else ("LoopBlock" if is_loop_pt else "BasicBlock"),
                code=stmt.code,
                kind=stmt.kind,
                is_decision=is_decision_pt,
                is_loop=is_loop_pt,
                has_unsafe=stmt.has_unsafe,
            )

            cfg.add_edge(prev_node, curr_node, edge_type="FLOW")

            if is_decision_pt:
                # Add conditional branch targets (true/false paths)
                then_node = f"{curr_node}_THEN"
                else_node = f"{curr_node}_ELSE"
                cfg.add_node(then_node, node_type="BranchPath", label="THEN")
                cfg.add_node(else_node, node_type="BranchPath", label="ELSE")

                cfg.add_edge(curr_node, then_node, edge_type="TRUE_BRANCH")
                cfg.add_edge(curr_node, else_node, edge_type="FALSE_BRANCH")

                # Rejoin node
                join_node = f"{curr_node}_JOIN"
                cfg.add_node(join_node, node_type="JoinBlock", label="JOIN")
                cfg.add_edge(then_node, join_node, edge_type="FLOW")
                cfg.add_edge(else_node, join_node, edge_type="FLOW")

                prev_node = join_node
            elif is_loop_pt:
                # Add loop latch edge back to header
                loop_header = f"{curr_node}_HEADER"
                cfg.add_node(loop_header, node_type="LoopHeader", label="HEADER")
                cfg.add_edge(curr_node, loop_header, edge_type="LOOP_ENTRY")
                cfg.add_edge(loop_header, curr_node, edge_type="LOOP_BACKEDGE")
                prev_node = loop_header
            else:
                prev_node = curr_node

        cfg.add_edge(prev_node, exit_node, edge_type="FLOW")

        # Compute McCabe's Cyclomatic Complexity
        # V(G) = Decision Points + Loop Points + 1
        complexity = branch_count + loop_count + 1

        # Or graph formula: E - N + 2P if connected
        E = cfg.number_of_edges()
        N = cfg.number_of_nodes()
        computed_complexity = max(1, E - N + 2)

        cfg.graph["cyclomatic_complexity"] = max(complexity, computed_complexity)
        cfg.graph["branch_count"] = branch_count
        cfg.graph["loop_count"] = loop_count

        return cfg

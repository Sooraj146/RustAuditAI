"""
Code Property Graph (CPG) Builder for RustAuditAI.
Synthesizes AST, CFG, and FLOG graph models into a unified intra-procedural program representation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import networkx as nx

from rustaudit.parser.rust_parser import FunctionAstInfo
from .ast_graph import ASTGraphBuilder
from .cfg_graph import CFGGraphBuilder
from .flog_graph import FLOGGraphBuilder


@dataclass
class CodePropertyGraph:
    """
    Container representing the multi-layered Code Property Graph for a Rust subroutine.
    """

    function_name: str
    ast: nx.DiGraph
    cfg: nx.DiGraph
    flog: nx.DiGraph
    unified_cpg: nx.DiGraph

    def summary(self) -> Dict[str, Any]:
        return {
            "function_name": self.function_name,
            "ast_nodes": self.ast.number_of_nodes(),
            "ast_edges": self.ast.number_of_edges(),
            "cfg_nodes": self.cfg.number_of_nodes(),
            "cfg_edges": self.cfg.number_of_edges(),
            "cyclomatic_complexity": self.cfg.graph.get("cyclomatic_complexity", 1),
            "flog_nodes": self.flog.number_of_nodes(),
            "flog_edges": self.flog.number_of_edges(),
            "clones": self.flog.graph.get("total_clones", 0),
            "allocations": self.flog.graph.get("total_allocations", 0),
            "unsafe_blocks": self.flog.graph.get("total_unsafe_blocks", 0),
            "cpg_nodes": self.unified_cpg.number_of_nodes(),
            "cpg_edges": self.unified_cpg.number_of_edges(),
        }


class CPGBuilder:
    """
    Builds the unified Code Property Graph combining AST, CFG, and FLOG layers.
    """

    def __init__(self):
        self.ast_builder = ASTGraphBuilder()
        self.cfg_builder = CFGGraphBuilder()
        self.flog_builder = FLOGGraphBuilder()

    def build_cpg(self, fn_info: FunctionAstInfo) -> CodePropertyGraph:
        ast = self.ast_builder.build_ast_graph(fn_info)
        cfg = self.cfg_builder.build_cfg_graph(fn_info)
        flog = self.flog_builder.build_flog_graph(fn_info)

        # Build unified CPG graph merging nodes and connecting cross-layer edges
        unified = nx.DiGraph()

        # Compose AST, CFG, and FLOG nodes
        for node, data in ast.nodes(data=True):
            unified.add_node(f"AST::{node}", layer="AST", **data)

        for node, data in cfg.nodes(data=True):
            unified.add_node(f"CFG::{node}", layer="CFG", **data)

        for node, data in flog.nodes(data=True):
            unified.add_node(f"FLOG::{node}", layer="FLOG", **data)

        # Copy intra-layer edges
        for u, v, data in ast.edges(data=True):
            unified.add_edge(f"AST::{u}", f"AST::{v}", **data)

        for u, v, data in cfg.edges(data=True):
            unified.add_edge(f"CFG::{u}", f"CFG::{v}", **data)

        for u, v, data in flog.edges(data=True):
            unified.add_edge(f"FLOG::{u}", f"FLOG::{v}", **data)

        # Add cross-layer connecting edges (Function root unification)
        ast_root = f"AST::fn_{fn_info.name}"
        cfg_entry = f"CFG::cfg_{fn_info.name}_ENTRY"
        flog_root = f"FLOG::flog_{fn_info.name}_SCOPE"

        if unified.has_node(ast_root) and unified.has_node(cfg_entry):
            unified.add_edge(ast_root, cfg_entry, edge_type="AST_TO_CFG")

        if unified.has_node(ast_root) and unified.has_node(flog_root):
            unified.add_edge(ast_root, flog_root, edge_type="AST_TO_FLOG")

        return CodePropertyGraph(
            function_name=fn_info.name,
            ast=ast,
            cfg=cfg,
            flog=flog,
            unified_cpg=unified,
        )

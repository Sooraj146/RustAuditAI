"""
AST Graph Builder for RustAuditAI.
Constructs a directed NetworkX graph representing the Abstract Syntax Tree of a Rust subroutine.
"""

from typing import Any, Dict
import networkx as nx
from rustaudit.parser.rust_parser import FunctionAstInfo, StatementSummary


class ASTGraphBuilder:
    """
    Builds a NetworkX DiGraph representing the functional AST of a Rust function.
    """

    def build_ast_graph(self, fn_info: FunctionAstInfo) -> nx.DiGraph:
        graph = nx.DiGraph()

        fn_node_id = f"fn_{fn_info.name}"
        graph.add_node(
            fn_node_id,
            node_type="FunctionDecl",
            name=fn_info.name,
            visibility=fn_info.visibility,
            is_unsafe=fn_info.is_unsafe,
            is_async=fn_info.is_async,
            output_type=fn_info.output_type,
            line_start=fn_info.line_start,
            line_end=fn_info.line_end,
        )

        # Signature Parameters Node
        params_node_id = f"{fn_node_id}_params"
        graph.add_node(params_node_id, node_type="ParamList", count=len(fn_info.inputs))
        graph.add_edge(fn_node_id, params_node_id, label="HAS_PARAMS")

        for idx, param in enumerate(fn_info.inputs):
            param_id = f"{params_node_id}_p{idx}"
            graph.add_node(param_id, node_type="Param", text=param)
            graph.add_edge(params_node_id, param_id, label="PARAM")

        # Function Body Node
        body_node_id = f"{fn_node_id}_body"
        graph.add_node(body_node_id, node_type="BlockStmt", stmt_count=len(fn_info.statements))
        graph.add_edge(fn_node_id, body_node_id, label="HAS_BODY")

        # Statement Nodes
        for idx, stmt in enumerate(fn_info.statements):
            stmt_id = f"{body_node_id}_stmt_{idx}"
            graph.add_node(
                stmt_id,
                node_type="Statement",
                kind=stmt.kind,
                code=stmt.code,
                has_clone=stmt.has_clone,
                has_unsafe=stmt.has_unsafe,
                has_allocation=stmt.has_allocation,
                index=idx,
            )
            graph.add_edge(body_node_id, stmt_id, label="CONTAINS_STMT")

        return graph

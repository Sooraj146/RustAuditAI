"""
Function-Level Ownership Graph (FLOG) Engine for RustAuditAI.
Constructs a domain-specific graph tracking variable allocations, moves, borrows, clones, and unsafe operations.
"""

import re
from typing import Dict, List, Set, Tuple
import networkx as nx
from rustaudit.parser.rust_parser import FunctionAstInfo, StatementSummary


class FLOGGraphBuilder:
    """
    Builds the Function-Level Ownership Graph (FLOG) for intra-procedural lifecycle evaluation.
    """

    def build_flog_graph(self, fn_info: FunctionAstInfo) -> nx.DiGraph:
        flog = nx.DiGraph()

        root_id = f"flog_{fn_info.name}_SCOPE"
        flog.add_node(
            root_id,
            node_type="FnScope",
            fn_name=fn_info.name,
            clone_count=fn_info.clone_count,
            allocation_count=fn_info.allocation_count,
            unsafe_block_count=fn_info.unsafe_block_count,
        )

        declared_vars: Set[str] = set()

        # Track parameters as initial owned or borrowed bindings
        for param in fn_info.inputs:
            clean_param = param.strip()
            param_var = clean_param.split(":")[0].replace("mut ", "").strip()
            is_borrow = "&" in clean_param
            is_mut_borrow = "&mut" in clean_param

            param_node_id = f"var_{param_var}"
            flog.add_node(
                param_node_id,
                node_type="BorrowBinding" if is_borrow else "OwnedBinding",
                var_name=param_var,
                is_mut=is_mut_borrow,
                is_borrow=is_borrow,
                raw_type=clean_param,
            )
            flog.add_edge(root_id, param_node_id, edge_type="SCOPE_BINDING")
            declared_vars.add(param_var)

        # Iterate statements to model allocations, clones, moves, and borrows
        for idx, stmt in enumerate(fn_info.statements):
            stmt_node_id = f"stmt_{idx}"

            # Detect let variable declarations: `let [mut] var_name = expr;`
            let_match = re.search(r'\blet\s+(?:mut\s+)?(\w+)\s*(?::\s*[^=]+)?\s*=\s*(.+)', stmt.code)
            if let_match:
                var_name = let_match.group(1)
                expr_code = let_match.group(2)
                var_node_id = f"var_{var_name}"

                # Determine variable binding category
                is_heap_alloc = any(kw in expr_code for kw in ["Box::new", "Vec::new", "String::from", ".to_vec", ".to_string"])
                is_clone = ".clone(" in expr_code
                is_mut_borrow = "&mut " in expr_code
                is_immut_borrow = "&" in expr_code and not is_mut_borrow

                binding_type = "HeapAllocation" if is_heap_alloc else ("ClonedBinding" if is_clone else "LocalBinding")

                flog.add_node(
                    var_node_id,
                    node_type=binding_type,
                    var_name=var_name,
                    is_heap_alloc=is_heap_alloc,
                    is_clone=is_clone,
                    code=stmt.code,
                )
                flog.add_edge(root_id, var_node_id, edge_type="DECLARES")
                declared_vars.add(var_name)

                # Check for source variable move or borrow relationships
                for src_var in list(declared_vars):
                    if src_var != var_name and re.search(r'\b' + re.escape(src_var) + r'\b', expr_code):
                        if is_clone:
                            flog.add_edge(src_var, var_node_id, edge_type="CLONED_FROM")
                        elif is_mut_borrow:
                            flog.add_edge(src_var, var_node_id, edge_type="MUTABLE_BORROW")
                        elif is_immut_borrow:
                            flog.add_edge(src_var, var_node_id, edge_type="IMMUTABLE_BORROW")
                        else:
                            flog.add_edge(src_var, var_node_id, edge_type="MOVED_TO")

            # Check for unsafe operations inside statement
            if stmt.has_unsafe or "unsafe" in stmt.code:
                unsafe_node_id = f"unsafe_op_{idx}"
                flog.add_node(
                    unsafe_node_id,
                    node_type="UnsafeOperation",
                    code=stmt.code,
                    index=idx,
                )
                flog.add_edge(root_id, unsafe_node_id, edge_type="CONTAINS_UNSAFE")

        # Summary graph metadata
        flog.graph["total_variables"] = len(declared_vars)
        flog.graph["total_clones"] = fn_info.clone_count
        flog.graph["total_allocations"] = fn_info.allocation_count
        flog.graph["total_unsafe_blocks"] = fn_info.unsafe_block_count

        return flog

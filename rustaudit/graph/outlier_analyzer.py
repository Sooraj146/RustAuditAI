"""
Graph Outlier Analyzer Engine for RustAuditAI.
Analyzes AST, CFG, and FLOG graph topologies to extract domain-specific outliers, anomalies, and structural hotspots.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from rustaudit.parser.rust_parser import FunctionAstInfo
from rustaudit.cwe import CWERegistry
from .cpg_builder import CodePropertyGraph


@dataclass
class GraphOutlierItem:
    graph_type: str  # "AST", "CFG", or "FLOG"
    severity: str    # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    title: str
    description: str
    affected_nodes: List[str] = field(default_factory=list)
    cwe_id: Optional[str] = None
    cwe_name: Optional[str] = None
    cwe_url: Optional[str] = None
    line_number: Optional[int] = None
    statement_code: Optional[str] = None
    remediation: Optional[str] = None


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

    def get_cwe_tags(self) -> List[Dict[str, Any]]:
        """
        Returns a deduplicated list of all CWE tags identified across the graph models.
        """
        tags: List[Dict[str, Any]] = []
        seen = set()
        for item in self.ast_outliers + self.cfg_outliers + self.flog_outliers:
            if item.cwe_id:
                key = (item.cwe_id, item.line_number)
                if key not in seen:
                    seen.add(key)
                    tags.append({
                        "cwe_id": item.cwe_id,
                        "name": item.cwe_name,
                        "severity": item.severity,
                        "url": item.cwe_url,
                        "line_number": item.line_number,
                        "statement_code": item.statement_code,
                        "message": item.title,
                        "remediation": item.remediation,
                    })
        return tags


class GraphOutlierAnalyzer:
    """
    Identifies structural and semantic outliers across Abstract Syntax Trees,
    Control Flow Graphs, and Function-Level Ownership Graphs, tagged with MITRE CWE indices.
    """

    def analyze_outliers(self, fn_info: FunctionAstInfo, cpg: CodePropertyGraph) -> GraphOutliersReport:
        ast_outliers: List[GraphOutlierItem] = []
        cfg_outliers: List[GraphOutlierItem] = []
        flog_outliers: List[GraphOutlierItem] = []

        # Helper to find first statement matching condition
        def find_stmt(predicate):
            for s in fn_info.statements:
                if predicate(s):
                    return s
            return None

        # --- 1. AST Graph Outliers ---
        if fn_info.is_unsafe:
            cwe_def = CWERegistry.get_definition("CWE-676")
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="CRITICAL",
                    title="Unsafe Function Scope Signature",
                    description=f"Function `{fn_info.name}` is declared with the `unsafe` keyword, bypassing rustc compile-time invariants for its entire body.",
                    affected_nodes=[f"fn_{fn_info.name}"],
                    cwe_id="CWE-676",
                    cwe_name=cwe_def.name if cwe_def else "Use of Potentially Dangerous Function",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/676.html",
                    line_number=fn_info.line_start,
                    statement_code=f"unsafe fn {fn_info.name}(...)",
                    remediation=cwe_def.remediation if cwe_def else "Remove `unsafe fn` signature and restrict unsafe operations to isolated blocks.",
                )
            )

        if len(fn_info.inputs) > 3:
            cwe_def = CWERegistry.get_definition("CWE-710")
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="LOW",
                    title="High Parameter Count Anomaly",
                    description=f"Function accepts {len(fn_info.inputs)} parameters. Consider grouping related parameters into a dedicated struct to improve maintainability.",
                    affected_nodes=[f"fn_{fn_info.name}_params"],
                    cwe_id="CWE-710",
                    cwe_name=cwe_def.name if cwe_def else "Improper Adherence to Coding Standards",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/710.html",
                    line_number=fn_info.line_start,
                    statement_code=f"fn {fn_info.name}({', '.join(fn_info.inputs[:3])}, ...)",
                    remediation="Group related parameters into a single context/options struct.",
                )
            )

        if len(fn_info.statements) > 10:
            cwe_def = CWERegistry.get_definition("CWE-710")
            ast_outliers.append(
                GraphOutlierItem(
                    graph_type="AST",
                    severity="LOW",
                    title="High AST Statement Density",
                    description=f"AST contains {len(fn_info.statements)} statements in a single subroutine block.",
                    affected_nodes=[f"fn_{fn_info.name}_body"],
                    cwe_id="CWE-710",
                    cwe_name=cwe_def.name if cwe_def else "Improper Adherence to Coding Standards",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/710.html",
                    line_number=fn_info.line_start,
                    statement_code=None,
                    remediation="Decompose the function into smaller, single-responsibility helper routines.",
                )
            )

        # --- 2. CFG Graph Outliers ---
        cc = cpg.cfg.graph.get("cyclomatic_complexity", 1)
        if cc > 5:
            cwe_def = CWERegistry.get_definition("CWE-710")
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="HIGH" if cc > 10 else "MEDIUM",
                    title=f"Cyclomatic Complexity Hotspot (V(G) = {cc})",
                    description=f"Control Flow Graph exhibits elevated branching complexity ({cc} independent execution paths). High risk of unhandled condition branches.",
                    affected_nodes=[n for n, d in cpg.cfg.nodes(data=True) if d.get("is_decision")],
                    cwe_id="CWE-710",
                    cwe_name=cwe_def.name if cwe_def else "Improper Adherence to Coding Standards",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/710.html",
                    line_number=fn_info.line_start,
                    statement_code=None,
                    remediation="Refactor nested decision branches using pattern matching or functional iterator chains.",
                )
            )

        decision_nodes = [n for n, d in cpg.cfg.nodes(data=True) if d.get("is_decision")]
        if decision_nodes and cc > 5:
            first_decision_stmt = find_stmt(lambda s: "if " in s.code or "match " in s.code)
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="LOW",
                    title="Conditional Branch Divergence Nodes",
                    description=f"Identified {len(decision_nodes)} branching decision points splitting control flow execution paths under elevated cyclomatic complexity (V(G) = {cc}).",
                    affected_nodes=decision_nodes,
                    cwe_id="CWE-710",
                    cwe_name="Improper Adherence to Coding Standards",
                    cwe_url="https://cwe.mitre.org/data/definitions/710.html",
                    line_number=first_decision_stmt.line_number if first_decision_stmt else fn_info.line_start,
                    statement_code=first_decision_stmt.code if first_decision_stmt else None,
                    remediation="Verify all branches handle exhaustive enum variants or default cases.",
                )
            )

        loop_nodes = [n for n, d in cpg.cfg.nodes(data=True) if d.get("is_loop")]
        if loop_nodes:
            first_loop_stmt = find_stmt(lambda s: "for " in s.code or "while " in s.code or "loop" in s.code)
            cwe_def = CWERegistry.get_definition("CWE-1075")
            cfg_outliers.append(
                GraphOutlierItem(
                    graph_type="CFG",
                    severity="LOW",
                    title="Cyclic Control Loop Back-Edge",
                    description=f"CFG contains {len(loop_nodes)} loop header latch node(s) introducing cyclic control flow edges.",
                    affected_nodes=loop_nodes,
                    cwe_id="CWE-1075",
                    cwe_name=cwe_def.name if cwe_def else "Unconditional Control Flow Transfer",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/1075.html",
                    line_number=first_loop_stmt.line_number if first_loop_stmt else fn_info.line_start,
                    statement_code=first_loop_stmt.code if first_loop_stmt else None,
                    remediation="Use functional iterators (`.filter()`, `.map()`, `.fold()`) to eliminate explicit loop back-edges.",
                )
            )

        # --- 3. FLOG Ownership Graph Outliers ---
        if fn_info.clone_count > 0:
            clone_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("is_clone")]
            first_clone_stmt = find_stmt(lambda s: s.has_clone or ".clone(" in s.code)
            cwe_def = CWERegistry.get_definition("CWE-400")
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="MEDIUM",
                    title="Deep Memory Copy (.clone()) Hotspot",
                    description=f"FLOG detected {fn_info.clone_count} explicit `.clone()` mutation node(s). High memory bandwidth overhead.",
                    affected_nodes=clone_nodes,
                    cwe_id="CWE-400",
                    cwe_name=cwe_def.name if cwe_def else "Uncontrolled Resource Consumption",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/400.html",
                    line_number=first_clone_stmt.line_number if first_clone_stmt else fn_info.line_start,
                    statement_code=first_clone_stmt.code if first_clone_stmt else None,
                    remediation=cwe_def.remediation if cwe_def else "Pass data by reference (`&T`, `&str`) instead of creating deep memory copies.",
                )
            )

        if fn_info.allocation_count > 0:
            alloc_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("is_heap_alloc")]
            first_alloc_stmt = find_stmt(lambda s: s.has_allocation or any(k in s.code for k in ("Box::new", "Vec::new", "String::from")))
            is_in_loop = fn_info.loop_count > 0
            cwe_id = "CWE-770" if is_in_loop else "CWE-400"
            cwe_def = CWERegistry.get_definition(cwe_id)
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="HIGH" if is_in_loop else "MEDIUM",
                    title="Micro-Heap Allocation Binding" + (" (Inside Loop)" if is_in_loop else ""),
                    description=f"FLOG mapped {fn_info.allocation_count} heap allocation node(s) (`Box::new`, `Vec::new`, `String::from`)." + (" Warning: Allocation occurs within loop scope." if is_in_loop else ""),
                    affected_nodes=alloc_nodes,
                    cwe_id=cwe_id,
                    cwe_name=cwe_def.name if cwe_def else "Uncontrolled Resource Consumption",
                    cwe_url=cwe_def.url if cwe_def else f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html",
                    line_number=first_alloc_stmt.line_number if first_alloc_stmt else fn_info.line_start,
                    statement_code=first_alloc_stmt.code if first_alloc_stmt else None,
                    remediation=cwe_def.remediation if cwe_def else "Stack-allocate bindings or reuse allocated buffers.",
                )
            )

        if fn_info.unsafe_block_count > 0:
            unsafe_nodes = [n for n, d in cpg.flog.nodes(data=True) if d.get("node_type") == "UnsafeOperation"]
            first_unsafe_stmt = find_stmt(lambda s: s.has_unsafe or "unsafe" in s.code)
            cwe_def = CWERegistry.get_definition("CWE-119")
            flog_outliers.append(
                GraphOutlierItem(
                    graph_type="FLOG",
                    severity="HIGH",
                    title="Unsafe Memory Lifecycle Scope",
                    description=f"FLOG maps {fn_info.unsafe_block_count} explicit unsafe block node(s) where lifetime & borrow safety checks are suspended.",
                    affected_nodes=unsafe_nodes,
                    cwe_id="CWE-119",
                    cwe_name=cwe_def.name if cwe_def else "Improper Restriction of Operations within the Bounds of a Memory Buffer",
                    cwe_url=cwe_def.url if cwe_def else "https://cwe.mitre.org/data/definitions/119.html",
                    line_number=first_unsafe_stmt.line_number if first_unsafe_stmt else fn_info.line_start,
                    statement_code=first_unsafe_stmt.code if first_unsafe_stmt else None,
                    remediation=cwe_def.remediation if cwe_def else "Replace `unsafe` block with safe reference abstractions.",
                )
            )

        return GraphOutliersReport(
            ast_outliers=ast_outliers,
            cfg_outliers=cfg_outliers,
            flog_outliers=flog_outliers,
        )

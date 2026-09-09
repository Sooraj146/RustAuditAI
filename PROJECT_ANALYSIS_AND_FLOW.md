# RustAuditAI — Comprehensive File-by-File Analysis & Execution Flow

> **Project Name:** RustAuditAI: Intra-Procedural Graph-Based Semantic Analysis & Multi-Dimensional Software Quality Assessment for Rust  
> **Repository Root:** `c:\Users\Admin\Desktop\Projects\RustAudit`  
> **Document Purpose:** Complete file-by-file specification covering **Usage**, **Importance**, **What it does**, **What it consists of**, and a complete **Filewise Project Execution Flow** mapping how runtime control transitions across files.

---

## Table of Contents
1. [Project Architectural Overview](#project-architectural-overview)
2. [Complete File-by-File Analysis](#complete-file-by-file-analysis)
   - [Root Files & Configuration](#1-root-files--configuration)
   - [Native Rust Parser Engine (`cargo_parser/`)](#2-native-rust-parser-engine-cargo_parser)
   - [Core Package & Web Server (`rustaudit/`)](#3-core-package--web-server-rustaudit)
   - [Rust Code Parsing Subsystem (`rustaudit/parser/`)](#4-rust-code-parsing-subsystem-rustauditparser)
   - [Graph Abstraction Engine (`rustaudit/graph/`)](#5-graph-abstraction-engine-rustauditgraph)
   - [MITRE CWE Taxonomies & Registry (`rustaudit/cwe/`)](#6-mitre-cwe-taxonomies--registry-rustauditcwe)
   - [RQI & Vector Metrics Engine (`rustaudit/metrics/`)](#7-rqi--vector-metrics-engine-rustauditmetrics)
   - [Explainable AI (XAI) & LLM Engine (`rustaudit/ai/`)](#8-explainable-ai-xai--llm-engine-rustauditai)
   - [Executive PDF Reporting Engine (`rustaudit/reports/`)](#9-executive-pdf-reporting-engine-rustauditreports)
   - [Web Dashboard Frontend (`rustaudit/web/`)](#10-web-dashboard-frontend-rustauditweb)
   - [Verification Test Suite & Samples (`tests/`)](#11-verification-test-suite--samples-tests)
3. [Filewise Project Execution Flow](#filewise-project-execution-flow)
   - [Flow A: CLI Batch Execution Flow (`main.py`)](#flow-a-cli-batch-execution-flow-mainpy)
   - [Flow B: Web UI & REST API Execution Flow (`server.py`)](#flow-b-web-ui--rest-api-execution-flow-serverpy)
   - [Flow C: Executive PDF Report Generation Flow](#flow-c-executive-pdf-report-generation-flow)
   - [Flow D: End-to-End Automated Test Flow](#flow-d-end-to-end-automated-test-flow)
4. [Cross-Module Dependency Matrix](#cross-module-dependency-matrix)

---

## Project Architectural Overview

RustAuditAI operates as an intra-procedural static analysis, graph modeling, and automated refactoring intelligence system for Rust code. The architecture is organized into four main layers:

```
[Rust Source Code (.rs)]
          │
          ▼
1. Parsing Layer (cargo_parser Rust Binary via `syn` OR fallback Python AST in `rust_parser.py`)
          │  Output: FunctionAstInfo & StatementSummary
          ▼
2. Graph Modeling Layer (`rustaudit/graph/`)
   ├── AST Graph Builder (Abstract Syntax Tree)
   ├── CFG Graph Builder (Control Flow Graph & McCabe Cyclomatic Complexity)
   ├── FLOG Graph Builder (Function-Level Ownership Graph: Clones, Allocations, Borrows)
   └── CPG Builder (Code Property Graph - Unifying AST, CFG, & FLOG via cross-layer edges)
          │
          ▼
3. Outlier & Weakness Identification Layer (`outlier_analyzer.py` & `cwe/registry.py`)
   └── Structural anomalies mapped to MITRE CWE IDs (CWE-119, CWE-400, CWE-710, etc.)
          │
          ▼
4. Metrics Synthesis Layer (`rustaudit/metrics/`)
   ├── QualityVectorCalculator (Safety, Performance, Maintainability, Security: 0-100)
   └── RQISynthesizer (Calculates composite RQI & applies dynamic non-linear penalties)
          │
   ┌──────┴──────────────────────────────────────────────────────┐
   │                                                             │
   ▼                                                             ▼
5. Explainable AI Engine (`rustaudit/ai/`)              6. Presentation & Delivery
   ├── XAIPromptBuilder (Deterministic CPG facts)         ├── CLI Output (`main.py`)
   ├── LLMClient (Google Gemini / Groq API)               ├── Web Dashboard (`server.py` + UI)
   └── XAIEngine (Extracts patches & diffs)               └── PDF Report (`pdf_generator.py`)
```

---

## Complete File-by-File Analysis

### 1. Root Files & Configuration

---

#### [`main.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/main.py)
* **Usage:** CLI entry point for command-line auditing. Run via:
  ```bash
  python main.py <path_to_rust_file.rs> [--explain]
  ```
* **Importance:** **Critical**. Serves as the standalone terminal runner and operational demonstration vehicle for batch/intra-procedural analysis without needing a web browser.
* **What it does:** Reads a target `.rs` file from disk, invokes `RustParser` to extract all functions, orchestrates `CPGBuilder` and `RQISynthesizer` per subroutine, prints formatted vector summaries, penalties, deductions, and optionally triggers `XAIEngine` to print LLM refactorings and code patches to standard output.
* **What it consists of:**
  - `main()` function: CLI argument parser, pipeline runner, and console logger.
  - Imports: `RustParser`, `CPGBuilder`, `RQISynthesizer`, `XAIEngine`.

---

#### [`requirements.txt`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/requirements.txt)
* **Usage:** Pip package dependency manifest. Installed via:
  ```bash
  pip install -r requirements.txt
  ```
* **Importance:** **High**. Defines the exact Python packages required to run the server, build graphs, contact LLMs, and run unit tests.
* **What it does:** Locks dependencies including `networkx` (graph modeling), `pydantic` (schema validation), `httpx` (async HTTP for LLM REST APIs), `rich` (CLI terminal styling), `fastapi` & `uvicorn` (web dashboard API backend), `python-dotenv` (reading `.env` keys), `reportlab` (PDF generation), and `pytest` (automated testing).
* **What it consists of:**
  - 8 core package declarations with version bounds.

---

#### [`RustAuditAI.pdf`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/RustAuditAI.pdf)
* **Usage:** Academic documentation, project report, and master specification reference.
* **Importance:** **Medium**. Serves as the formal reference manual and academic report (MCA Mini Project Report, APJ Abdul Kalam Technological University) detailing theoretical underpinnings, literature review, and system requirements.
* **What it does:** Provides the full formal background on intra-procedural static analysis, Code Property Graphs (CPGs), Function-Level Ownership Graphs (FLOGs), and Rust Quality Index formulas.
* **What it consists of:**
  - Compiled PDF document containing project chapters, diagrams, and theoretical algorithms.

---

#### [`srs_content.txt`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/srs_content.txt)
* **Usage:** Textual extraction of the project's Software Requirements Specification (SRS) and project report.
* **Importance:** **Medium**. Quick searchable reference for engineering requirements, mathematical models, weights, and functional modules.
* **What it does:** Outlines the core specifications, mathematical formulas for the RQI (30% Safety, 25% Performance, 25% Maintainability, 20% Security), non-linear penalty thresholds, and UI specifications.
* **What it consists of:**
  - Plaintext pages extracted from the formal project report.

---

#### [`SKILLS.md`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/SKILLS.md)
* **Usage:** Development guide and UI design skill documentation.
* **Importance:** **Low / Supportive**. Provides styling guidelines, OKLCH color palettes, typography principles, and interface aesthetics used when designing the web dashboard.
* **What it does:** Acts as an internal design playbook for crafting distinctive, accessible, non-generic frontend layouts and visual hierarchies.
* **What it consists of:**
  - Markdown instructions on design philosophy, color spaces, ambient lighting, and UX patterns.

---

### 2. Native Rust Parser Engine (`cargo_parser/`)

---

#### [`cargo_parser/Cargo.toml`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/cargo_parser/Cargo.toml)
* **Usage:** Rust Cargo package configuration for building the high-speed native parser. Built via:
  ```bash
  cd cargo_parser && cargo build --release
  ```
* **Importance:** **High**. Manages the compiler configurations and Rust crate dependencies for AST traversal.
* **What it does:** Declares the crate name `cargo_parser` (Rust 2021 edition) and pulls in the official `syn` crate with AST visitor features, `quote`, `proc-macro2`, `serde`, and `serde_json`.
* **What it consists of:**
  - Package metadata (`cargo_parser v0.1.0`).
  - Dependency listings: `syn 2.0`, `serde 1.0`, `serde_json 1.0`, `quote 1.0`, `proc-macro2 1.0`.

---

#### [`cargo_parser/Cargo.lock`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/cargo_parser/Cargo.lock)
* **Usage:** Cargo lockfile for deterministic, reproducible native binary compilation.
* **Importance:** **Medium**. Locks exact transitive crate versions (such as `unicode-ident`, `proc-macro2`, etc.).
* **What it does:** Guarantees that compilation of `cargo_parser` is completely consistent across environments.
* **What it consists of:**
  - Concrete dependency tree lock metadata generated by Cargo.

---

#### [`cargo_parser/src/main.rs`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/cargo_parser/src/main.rs)
* **Usage:** Executable Rust program invoked as a subprocess by Python's `RustParser`. It accepts either a file path argument or raw Rust source code through `stdin`, and outputs JSON to `stdout`.
* **Importance:** **Critical**. Provides 100% rustc-accurate parsing of Rust subroutines using the official `syn` AST parser, eliminating regex limitations for complex macros, lifetimes, and nesting.
* **What it does:**
  - Parses Rust source code into a `syn::File` syntax tree.
  - Implements a `FunctionVisitor` (using `syn::visit::Visit`) to discover functions (`ItemFn`).
  - Implements an `ExprVisitor` to detect allocations (`Box::new`, `Vec::new`, `String::from`, `.to_vec()`), clones (`.clone()`), unsafe blocks (`unsafe { ... }`), branches (`if`, `match`), loops (`for`, `while`, `loop`), and reference borrows (`&`, `&mut`).
  - Emits a structured JSON payload containing function signatures, line ranges, metric counters, and individual statements.
* **What it consists of:**
  - Structs: `AnalysisOutput`, `FunctionAstInfo`, `StatementSummary`.
  - Visitor implementations: `FunctionVisitor`, `ExprVisitor`.
  - Helper functions: `analyze_fn_body`, `get_stmt_kind`, `get_expr_kind`, `inspect_stmt`, `main`.

---

### 3. Core Package & Web Server (`rustaudit/`)

---

#### [`rustaudit/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/__init__.py)
* **Usage:** Package root initializer. Imported when accessing `rustaudit`.
* **Importance:** **Low / Standard**. Designates `rustaudit` as a Python package.
* **What it does:** Defines package-level metadata and `__version__ = "0.1.0"`.
* **What it consists of:**
  - Module docstring and version definition.

---

#### [`rustaudit/server.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/server.py)
* **Usage:** FastAPI application and web dashboard server. Launched via:
  ```bash
  python rustaudit/server.py
  # OR: uvicorn rustaudit.server:app --reload --port 8000
  ```
* **Importance:** **Critical**. Serves as the central API gateway and web backend for the entire graphical interactive platform.
* **What it does:**
  - Hosts the single-page web dashboard (`GET /`).
  - Handles source file uploads with extension and encoding validation (`POST /api/upload`).
  - Executes the full analysis pipeline on code payloads (`POST /api/analyze`), returning JSON graph data, RQI scores, CWE tags, and XAI refactoring patches.
  - Generates and downloads executive publication-grade audit PDFs (`POST /api/export/pdf`).
  - Mounts static CSS and JS assets.
* **What it consists of:**
  - FastAPI app instance and router declarations.
  - Pydantic models: `AnalyzeRequest`, `ExportReportRequest`.
  - Endpoints: `get_dashboard()`, `upload_file()`, `analyze_code()`, `export_pdf_report()`.
  - Integrations: Initialized instances of `RustParser`, `CPGBuilder`, `GraphOutlierAnalyzer`, `RQISynthesizer`, `XAIEngine`, and `RustAuditPDFReportGenerator`.

---

### 4. Rust Code Parsing Subsystem (`rustaudit/parser/`)

---

#### [`rustaudit/parser/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/parser/__init__.py)
* **Usage:** Exposes parsing interfaces to callers.
* **Importance:** **Low / Standard**. Clean package interface.
* **What it does:** Re-exports `RustParser`, `FunctionAstInfo`, and `AnalysisResult`.
* **What it consists of:**
  - `__all__` export list and import statements.

---

#### [`rustaudit/parser/rust_parser.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/parser/rust_parser.py)
* **Usage:** Imported by `main.py` and `server.py` to parse any Rust code string or file.
* **Importance:** **Critical**. The fundamental ingress component that ingests raw source text and turns it into structured function entities for graph construction.
* **What it does:**
  - Implements a hybrid dual-engine parsing strategy:
    1. **Primary**: Tries to invoke compiled binary `cargo_parser/target/release/cargo_parser.exe` via `subprocess.run` with JSON communication.
    2. **Fallback**: If the Rust binary is not built or unavailable, automatically falls back to an internal pure-Python regex AST parser (`_python_fallback_parse`).
  - Extracts visibility, mutability, function signatures, statement blocks, loop counts, clone calls, unsafe blocks, and memory allocations.
  - Resolves statement-to-source 1-based line numbers via `_resolve_statement_lines`.
* **What it consists of:**
  - Dataclasses: `StatementSummary`, `FunctionAstInfo`, `AnalysisResult`.
  - Class `RustParser`:
    - `parse_file(file_path)`
    - `parse_code(code, file_path)`
    - `_python_fallback_parse(code, file_path)`
    - `_extract_block(code, start_index, lines)`
    - `_extract_statements(body_code)`
    - `_resolve_statement_lines(code, functions)`

---

### 5. Graph Abstraction Engine (`rustaudit/graph/`)

---

#### [`rustaudit/graph/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/__init__.py)
* **Usage:** Exposes all graph modeling builders and data models.
* **Importance:** **Low / Standard**. Package abstraction layer.
* **What it does:** Re-exports `ASTGraphBuilder`, `CFGGraphBuilder`, `FLOGGraphBuilder`, `CPGBuilder`, `CodePropertyGraph`, `GraphOutlierAnalyzer`, and `GraphOutliersReport`.
* **What it consists of:**
  - Package exports and module definitions.

---

#### [`rustaudit/graph/ast_graph.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/ast_graph.py)
* **Usage:** Instantiated by `CPGBuilder` to build the syntactic hierarchy graph.
* **Importance:** **High**. Models the structural syntax tree of the Rust subroutine.
* **What it does:**
  - Translates `FunctionAstInfo` into a directed `networkx.DiGraph`.
  - Creates the root `FunctionDecl` node, signature `ParamList` node, individual parameter nodes, function `BlockStmt` body node, and sequentially connected `Statement` nodes.
  - Decorates nodes with attributes such as `node_type`, `has_clone`, `has_unsafe`, and statement indices.
* **What it consists of:**
  - Class `ASTGraphBuilder`: `build_ast_graph(fn_info) -> nx.DiGraph`.

---

#### [`rustaudit/graph/cfg_graph.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/cfg_graph.py)
* **Usage:** Instantiated by `CPGBuilder` to construct control flow topology and calculate McCabe Cyclomatic Complexity.
* **Importance:** **High**. Measures execution path branching, loops, and condition structures.
* **What it does:**
  - Generates `ENTRY` and `EXIT` nodes for each subroutine.
  - Constructs basic blocks, decision blocks (`Expr(If)`, `Expr(Match)`), branch paths (`THEN`, `ELSE`), join blocks, and cyclic loop back-edges (`LoopHeader`, `LOOP_BACKEDGE`).
  - Computes McCabe's Cyclomatic Complexity:
    $$V(G) = E - N + 2P \quad \text{or} \quad V(G) = \text{Branch Count} + \text{Loop Count} + 1$$
  - Stores $V(G)$ in `cfg.graph["cyclomatic_complexity"]`.
* **What it consists of:**
  - Class `CFGGraphBuilder`: `build_cfg_graph(fn_info) -> nx.DiGraph`.

---

#### [`rustaudit/graph/flog_graph.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/flog_graph.py)
* **Usage:** Instantiated by `CPGBuilder` to model Rust-specific memory ownership semantics.
* **Importance:** **Critical**. Domain-specific innovation that models Rust's affine type system, borrowing, and allocations at the function level.
* **What it does:**
  - Builds the **Function-Level Ownership Graph (FLOG)**.
  - Tracks variable lifecycles: owned bindings (`OwnedBinding`), mutable/immutable borrows (`BorrowBinding`, `MUTABLE_BORROW`, `IMMUTABLE_BORROW`), moves (`MOVED_TO`), cloned duplicates (`ClonedBinding`, `CLONED_FROM`), and heap allocations (`HeapAllocation`).
  - Links unsafe blocks (`UnsafeOperation`) to the specific variables accessed inside them (`ACCESSED_IN_UNSAFE`).
* **What it consists of:**
  - Class `FLOGGraphBuilder`: `build_flog_graph(fn_info) -> nx.DiGraph`.

---

#### [`rustaudit/graph/cpg_builder.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/cpg_builder.py)
* **Usage:** Invoked by `main.py` and `server.py` to synthesize all graph layers into a single multi-layered graph.
* **Importance:** **Critical**. Synthesizes AST, CFG, and FLOG into the final Code Property Graph (CPG).
* **What it does:**
  - Orchestrates `ASTGraphBuilder`, `CFGGraphBuilder`, and `FLOGGraphBuilder`.
  - Merges their nodes into a unified `DiGraph` using namespace prefixes (`AST::`, `CFG::`, `FLOG::`).
  - Injects **cross-layer semantic edges**:
    - `AST_TO_CFG` (Root control link)
    - `AST_TO_FLOG` (Root ownership link)
    - `AST_TO_CFG_STMT` (Statement controls basic block)
    - `CFG_TO_FLOG_UNSAFE` & `AST_TO_FLOG_UNSAFE` (Execution and containment of unsafe operations)
    - `CFG_TO_FLOG_BIND` & `AST_TO_FLOG_DECL` (Binding and declaration of variables across control flow and syntax)
  - Produces `CodePropertyGraph` with summary statistics.
* **What it consists of:**
  - Dataclass `CodePropertyGraph`: holds `ast`, `cfg`, `flog`, `unified_cpg`, and `summary()`.
  - Class `CPGBuilder`: `build_cpg(fn_info) -> CodePropertyGraph`.

---

#### [`rustaudit/graph/outlier_analyzer.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/graph/outlier_analyzer.py)
* **Usage:** Invoked by `server.py` during code analysis to detect topological anomalies across graphs.
* **Importance:** **High**. Connects graph properties directly to MITRE CWE security and quality vulnerabilities.
* **What it does:**
  - Traverses the AST, CFG, and FLOG to identify structural hotspots:
    - **AST Outliers:** Unsafe function declarations (CWE-676), excessive argument counts (CWE-710), high statement density (CWE-710).
    - **CFG Outliers:** Cyclomatic complexity hotspots $V(G) > 5$ or $> 10$ (CWE-710), branch divergences, cyclic loop latches (CWE-1075).
    - **FLOG Outliers:** Explicit memory duplication `.clone()` (CWE-400), micro-heap allocations inside loop structures (CWE-770), unsafe block scopes (CWE-119).
  - Associates each outlier with line numbers, code snippets, severity ratings, and remediation instructions.
* **What it consists of:**
  - Dataclasses: `GraphOutlierItem`, `GraphOutliersReport`.
  - Class `GraphOutlierAnalyzer`: `analyze_outliers(fn_info, cpg) -> GraphOutliersReport`.

---

### 6. MITRE CWE Taxonomies & Registry (`rustaudit/cwe/`)

---

#### [`rustaudit/cwe/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/cwe/__init__.py)
* **Usage:** Package export layer for CWE definitions.
* **Importance:** **Low / Standard**. Clean imports.
* **What it does:** Exposes `CWEDefinition`, `CWETag`, and `CWERegistry`.
* **What it consists of:**
  - Module docstring and exports.

---

#### [`rustaudit/cwe/registry.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/cwe/registry.py)
* **Usage:** Imported by `vector_calculators.py`, `outlier_analyzer.py`, `prompt_builder.py`, and `pdf_generator.py`.
* **Importance:** **Critical**. The authoritative database of vulnerability definitions, official MITRE URLs, severities, and remediation strategies.
* **What it does:**
  - Maintains `CATALOG`: maps CWE identifiers to `CWEDefinition` instances:
    - `CWE-119`: Buffer bounds & unsafe block restriction
    - `CWE-476`: NULL/dangling raw pointer dereference
    - `CWE-416`: Use-after-free
    - `CWE-252`: Unchecked return value (`.unwrap()` / `.expect()`)
    - `CWE-129`: Improper slice/array indexing
    - `CWE-400`: Uncontrolled resource consumption (`.clone()`, heap allocation)
    - `CWE-770`: Allocation without limits (allocations in loops)
    - `CWE-710`: Coding standards & cyclomatic complexity
    - `CWE-1075`: Unconditional control flow transfers
    - `CWE-676`: Potentially dangerous functions (`unsafe fn`)
    - `CWE-703`: Exceptional condition handling
  - Maintains `DETECTION_MAP`: maps internal detection triggers to official CWE IDs.
  - Factory methods: `create_tag`, `tag_from_detection`, `get_definition`.
* **What it consists of:**
  - Dataclasses: `CWEDefinition`, `CWETag`.
  - Class `CWERegistry`: dictionary catalog, detection mapping, and query methods.

---

### 7. RQI & Vector Metrics Engine (`rustaudit/metrics/`)

---

#### [`rustaudit/metrics/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/metrics/__init__.py)
* **Usage:** Package export layer for metrics calculation.
* **Importance:** **Low / Standard**.
* **What it does:** Re-exports `QualityVectorCalculator`, `VectorScores`, `RQISynthesizer`, and `RQISummary`.
* **What it consists of:**
  - Module exports.

---

#### [`rustaudit/metrics/vector_calculators.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/metrics/vector_calculators.py)
* **Usage:** Instantiated by `RQISynthesizer` to score the 4 quality dimensions.
* **Importance:** **Critical**. Implements the mathematical deduction algorithms that convert graph structures and statement patterns into numerical quality metrics (0 to 100).
* **What it does:**
  - Computes four distinct vector scores:
    1. **Safety (0-100):** Starts at 100; penalizes `unsafe fn` (-30 pts, CWE-676), `unsafe` blocks (-15 pts each, CWE-119), raw pointer calls `as_ptr`/`as_mut_ptr` (-10 pts, CWE-476).
    2. **Performance (0-100):** Starts at 100; penalizes `.clone()` calls (-15 pts each, CWE-400), micro-heap allocations `Box`/`Vec`/`String` (-10 pts each, CWE-400), heap allocations inside loop bodies (-15 pts, CWE-770).
    3. **Maintainability (0-100):** Starts at 100; penalizes high cyclomatic complexity $V(G) > 5$ or $V(G) > 10$ (CWE-710), subroutines $> 50$ lines (-20 pts, CWE-710), statement density $> 12$ statements (-10 pts, CWE-710).
    4. **Security (0-100):** Starts at 100; penalizes `.unwrap()`/`.expect()` panic hazards (-12 pts, CWE-252), direct unvalidated slice indexing `arr[i]` (-10 pts, CWE-129), unsafe boundary exposure (-15 pts, CWE-119).
  - Populates structured `VectorDeduction` records with line numbers, statement code, penalty points, severity, and remediation advice.
* **What it consists of:**
  - Dataclasses: `VectorDeduction`, `VectorScores`.
  - Class `QualityVectorCalculator`: `calculate_vectors(fn_info, cpg) -> VectorScores`.

---

#### [`rustaudit/metrics/rqi_synthesizer.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/metrics/rqi_synthesizer.py)
* **Usage:** Invoked by `main.py` and `server.py` to synthesize final composite scores and determine grades.
* **Importance:** **Critical**. The core scoring synthesis engine of RustAuditAI.
* **What it does:**
  - Implements the weighted Rust Quality Index formula:
    $$\text{Base RQI} = 0.30 \times \text{Safety} + 0.25 \times \text{Performance} + 0.25 \times \text{Maintainability} + 0.20 \times \text{Security}$$
  - Evaluates non-linear safety & performance penalty rules:
    - If $\text{Safety} < 60.0$, applies a **15% cross-vector penalty** ($\text{Base RQI} \times 0.85$).
    - If $\text{Performance} < 50.0$, applies a **10% penalty** ($\text{Base RQI} \times 0.90$).
  - Maps final RQI score to standardized grades:
    - $\ge 90$: **A+ (Idiomatic & Robust)**
    - $\ge 80$: **A (Good Quality)**
    - $\ge 70$: **B (Acceptable)**
    - $\ge 60$: **C (Needs Refactoring)**
    - $\ge 50$: **D (High Risk / Inefficient)**
    - $< 50$: **F (Critical Vulnerability / Inefficient)**
  - Collects CWE summaries and tag aggregations.
* **What it consists of:**
  - Dataclass `RQISummary`: `function_name`, `rqi_score`, `grade`, `vectors`, `penalty_applied`, `penalty_reasons`, `structured_deductions`, `get_cwe_tags()`, `get_cwe_summary()`, `to_dict()`.
  - Class `RQISynthesizer`: weights constants, `compute_rqi(fn_info, cpg) -> RQISummary`.

---

### 8. Explainable AI (XAI) & LLM Engine (`rustaudit/ai/`)

---

#### [`rustaudit/ai/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/ai/__init__.py)
* **Usage:** Package exports for AI modules.
* **Importance:** **Low / Standard**.
* **What it does:** Exposes `LLMClient`, `XAIPromptBuilder`, `XAIEngine`, and `XAIReport`.
* **What it consists of:**
  - Module exports.

---

#### [`rustaudit/ai/prompt_builder.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/ai/prompt_builder.py)
* **Usage:** Invoked by `XAIEngine` to construct mathematically grounded prompts.
* **Importance:** **High**. Prevents LLM hallucinations by grounding the prompt strictly in deterministic CPG graph facts and RQI deductions.
* **What it does:**
  - Embeds strict system instructions enforcing functional invariance, function decomposition, 100% safety, zero unnecessary allocations/clones, and defensive error handling.
  - Injects target source code, AST node/edge counts, CFG cyclomatic complexity, FLOG allocation/clone counts, active deductions, and MITRE CWE tags with line numbers.
  - Mandates a strict 3-part Markdown output format:
    1. Root Cause Explanation (by CWE ID)
    2. Proposed Idiomatic Refactored Patch (full Rust code)
    3. Estimated Optimization Metrics (projected vector gains)
* **What it consists of:**
  - Class `XAIPromptBuilder`: `SYSTEM_PROMPT` constant, `build_prompt(...) -> str`.

---

#### [`rustaudit/ai/llm_client.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/ai/llm_client.py)
* **Usage:** Network client used by `XAIEngine` to communicate with LLM inference APIs.
* **Importance:** **High**. Provides resilient multi-provider LLM connectivity.
* **What it does:**
  - Automatically loads `.env` configuration for API keys.
  - Supports **Google Gemini API** (models: `gemini-3.7-flash`, `gemini-3.5-flash`, `gemma-4-26b-a4b-it`) via direct REST POST to `generativelanguage.googleapis.com`.
  - Supports **Groq API** (models: `openai/gpt-oss-120b`, `groq/compound`, `qwen/qwen3.6-27b`, etc.) as an instant high-speed fallback.
  - Handles failovers, model fallbacks, temperature tuning ($0.2$ for deterministic code refactoring), and error reporting.
* **What it consists of:**
  - Class `LLMClient`: `generate()`, `_call_gemini()`, `_call_groq()`.

---

#### [`rustaudit/ai/xai_engine.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/ai/xai_engine.py)
* **Usage:** Orchestrated by `main.py` (when `--explain` is passed) and `server.py` (when `explain: true`).
* **Importance:** **Critical**. The top-level AI coordination module.
* **What it does:**
  - Checks if the function already has a perfect score ($100.0$ RQI, no penalties); if so, skips LLM calls and returns an optimal quality statement.
  - Otherwise, prompts the LLM through `XAIPromptBuilder` and `LLMClient`.
  - Parses the raw LLM response using resilient regex extractors:
    - `_extract_code_block`: Isolates the pure Rust code patch specifically prioritizing Section 2 (`Proposed Idiomatic Refactored Patch`) with flexible fence matching (`r'```(?:rust|rs)?\s*\n?(.*?)\n?```'`) to prevent capturing inline snippets from Section 1.
    - `_extract_explanation`: Extracts root cause analysis.
    - `_extract_metrics`: Extracts optimization gains or builds mathematical default estimates.
    - `_generate_fallback_code`: Synthesizes clean, compilable idiomatic Rust code if the LLM output is missing a code block.
    - `_generate_deterministic_fallback`: Resilient offline fallback synthesizing structured root-cause insights and compilable refactored patches directly from CPG and RQI deductions if external LLM requests time out or fail.
    - `_generate_diff`: Uses Python's `difflib.unified_diff` to compute a unified diff between original code and proposed refactored patch.
* **What it consists of:**
  - Dataclass `XAIReport`: `function_name`, `explanation`, `refactored_code`, `diff_text`, `metrics_summary`, `raw_response`.
  - Class `XAIEngine`: `generate_explanation(...) -> XAIReport`, `_generate_fallback_code(...)`, `_generate_deterministic_fallback(...)`.

---

### 9. Executive PDF Reporting Engine (`rustaudit/reports/`)

---

#### [`rustaudit/reports/__init__.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/reports/__init__.py)
* **Usage:** Exposes the reporting subsystem.
* **Importance:** **Low / Standard**.
* **What it does:** Re-exports `RustAuditPDFReportGenerator` and helper function `generate_pdf_report`.
* **What it consists of:**
  - Module exports.

---

#### [`rustaudit/reports/pdf_generator.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/reports/pdf_generator.py)
* **Usage:** Invoked by `server.py` at `/api/export/pdf` to generate downloadable audit reports.
* **Importance:** **High**. Delivers publication-grade compliance documents complying with SRS §4.6.5.
* **What it does:**
  - Generates self-contained, multi-page, publication-grade executive audit PDF documents using ReportLab Platypus.
  - Implements a custom `NumberedCanvas` performing a two-pass calculation for running headers, rule dividers, confidential watermarks, and accurate "Page X of Y" pagination.
  - Renders 5 distinct executive sections:
    1. Header banner and metadata block (filename, date, qualifiers, line range).
    2. Executive RQI Scorecard & Four Vectors Matrix table.
    3. MITRE CWE Weaknesses counter strip (Total, Critical, High, Medium, Low).
    4. Quality Deductions & Weakness Catalog with exact source line numbers, code snippets, and actionable remediation instructions.
    5. Code Property Graph topology metrics table and XAI refactoring diffs.
* **What it consists of:**
  - Class `NumberedCanvas(canvas.Canvas)`.
  - Class `RustAuditPDFReportGenerator`: styling dictionary, table layout generators, and `generate(...) -> bytes`.
  - Convenience wrapper `generate_pdf_report(...)`.

---

### 10. Web Dashboard Frontend (`rustaudit/web/`)

---

#### [`rustaudit/web/templates/index.html`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/web/templates/index.html)
* **Usage:** The single-page application (SPA) HTML layout served at `GET /`.
* **Importance:** **High**. The user interface structure through which developers interact with the platform.
* **What it does:**
  - Provides a two-column desktop workstation layout:
    - **Left Column:** Source code editor with line numbering, sample code loader button, drag-and-drop file upload overlay (`.rs`), and an AI Refactoring toggle.
    - **Right Column:** Tabbed audit results panel featuring:
      - Function selector tabs (for files containing multiple subroutines).
      - RQI radial circular score gauge and grade badge.
      - Four quality vector progress bars (Safety, Performance, Maintainability, Security).
      - MITRE CWE Weaknesses counter pills (Critical, High, Medium, Low).
      - Detailed deductions list with line tags and remediation cards.
      - Graph metrics summary (AST, CFG, FLOG, Unified CPG).
      - Interactive Graph Visualization Canvas powered by Vis.js (interactive nodes and edges for AST, CFG, FLOG, and CPG).
      - Explainable AI Refactoring panel with side-by-side diff viewer and copy patch button.
      - "Export Executive PDF Report" action button.
* **What it consists of:**
  - HTML5 markup, SVG icons, Vis.js CDN link, layout sections, modal overlays.

---

#### [`rustaudit/web/static/css/style.css`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/web/static/css/style.css)
* **Usage:** Loaded by `index.html` to style the web UI.
* **Importance:** **Medium**. Implements modern dark-mode aesthetics.
* **What it does:**
  - Defines CSS variables for slate, navy, sky-blue, emerald, amber, and crimson colors.
  - Styles code editors, custom scrollbars, SVG gauge animations, badge components, diff syntax highlighting (red deletion, green insertion), and responsive breakpoints.
* **What it consists of:**
  - CSS rules, utility classes, grid layouts, and keyframe animations.

---

#### [`rustaudit/web/static/js/app.js`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/rustaudit/web/static/js/app.js)
* **Usage:** Loaded by `index.html` to handle browser client logic, user events, and API communication.
* **Importance:** **Critical**. Drives the entire client-side interactivity, state management, and network requests.
* **What it does:**
  - Manages application state: current code content, analysis payload, active function tab, active graph layer.
  - Handles drag-and-drop and manual file uploads (`/api/upload`).
  - Dispatches analysis queries (`/api/analyze`) with loading spinners and error handling.
  - Renders the interactive Vis.js Network diagram with color-coded nodes and edge labels (AST in blue, CFG in amber, FLOG in emerald, cross-layer CPG edges in violet).
  - Updates radial score gauge SVGs, quality vector meters, and CWE tags.
  - Features robust XAI Markdown explanation card parsing:
    - Splits top-level diagnostic points strictly at line boundaries (`(?:^|\n)\s*(?=\d+\.\s*(?:\*\*|[A-Z]))`) to prevent numbers inside prose (e.g. `exceeded 10. If...`) from creating false cards.
    - Sanitizes lingering markdown URLs (`((https://...))`) from card titles.
    - Implements prose safeguards that merge unheaded numeric lines back into the preceding insight.
  - Renders code patches with 1-click clipboard copy functionality and handles PDF download triggering (`/api/export/pdf`).
* **What it consists of:**
  - Event listeners: `analyzeBtn`, `uploadFileBtn`, `loadSampleBtn`, `exportPdfBtn`, `copyPatchBtn`.
  - State variables: `currentAnalysisData`, `activeFnIndex`, `networkInstance`.
  - Functions: `renderFunctionAudit()`, `renderGraph()`, `renderXAIExplanation()`, `updateScoreGauge()`.

---

### 11. Verification Test Suite & Samples (`tests/`)

---

#### [`tests/samples/sample_func.rs`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/samples/sample_func.rs)
* **Usage:** Test fixture used across multiple test modules.
* **Importance:** **Medium**. Realistic test case containing intentional anti-patterns.
* **What it does:**
  - Provides sample Rust functions:
    1. `process_user_data`: Contains `.clone()`, `Box::new()`, an `unsafe` block with raw pointer `.as_ptr()`. Evaluates to 83.8 RQI.
    2. `calculate_metrics`: Clean, idiomatic iterator loop with no unsafe code. Evaluates to 100.0 RQI.
* **What it consists of:**
  - Valid Rust source code subroutines with contrasting quality attributes.

---

#### [`tests/samples/penalty_low_rqi.rs`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/samples/penalty_low_rqi.rs)
* **Usage:** Sample problem file demonstrating low quality and non-linear penalties.
* **Importance:** **High**. Calibrated test fixture for the Non-Linear Penalty Matrix.
* **What it does:**
  - Demonstrates severe quality degradation:
    - Function marked `unsafe fn` (CWE-676, -30 pts).
    - Contains explicit `unsafe {}` block (CWE-119, -15 pts).
    - Raw pointer dereference operation (CWE-476, -10 pts).
    - Redundant `.clone()` calls causing heap memory duplication (CWE-400, -30 pts).
    - Micro-heap allocations `Box::new` and `Vec::new` (CWE-400, -20 pts).
    - Micro-allocations inside loop scopes (CWE-770, -15 pts).
  - Evaluates to **Safety = 45.0** (< 60.0 threshold) and **Performance = 35.0** (< 50.0 threshold), triggering compound cross-vector penalty deductions ($0.85 \times 0.90$).
  - Evaluates to **49.15 / 100 RQI (Grade D / F)**.
* **What it consists of:**
  - Rust subroutine `pub unsafe fn unsafe_buffer_mutator(...) -> Vec<u8>`.

---

#### [`tests/samples/moderate_rqi.rs`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/samples/moderate_rqi.rs)
* **Usage:** Sample problem file demonstrating moderate code quality without critical failures.
* **Importance:** **High**. Calibrated test fixture for Grade B (Acceptable) quality.
* **What it does:**
  - Demonstrates moderate performance clones and unchecked direct slice indexing:
    - Redundant `.clone()` calls (CWE-400, -30 pts).
    - Micro-heap allocations (CWE-400, -10 pts).
    - Multiple direct slice indexings `arr[i]` without defensive `.get()` bounds checking (CWE-129, -60 pts).
  - Maintains **Safety = 100.0** ($\ge 60.0$) and **Performance = 60.0** ($\ge 50.0$), ensuring **no penalties** are applied.
  - Evaluates to **78.00 / 100 RQI (Grade B)**.
* **What it consists of:**
  - Rust subroutine `pub fn process_matrix_cells(...) -> Vec<i32>`.

---

#### [`tests/samples/optimal_rqi.rs`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/samples/optimal_rqi.rs)
* **Usage:** Sample problem file demonstrating peak idiomatic Rust code quality.
* **Importance:** **High**. Calibrated test fixture for Grade A+ (Idiomatic & Robust).
* **What it does:**
  - Demonstrates zero-cost borrowed references (`&[i32]`), functional iterator chains (`.iter().filter().map().sum()`), zero allocations, no `unsafe` blocks, and low cyclomatic complexity.
  - Incurs **0 quality deductions** across all 4 quality vectors.
  - Evaluates to **100.00 / 100 RQI (Grade A+)**.
* **What it consists of:**
  - Rust subroutine `pub fn sum_even_squares(numbers: &[i32]) -> i64`.

---

#### [`tests/test_parser.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_parser.py)
* **Usage:** Run via `pytest tests/test_parser.py`.
* **Importance:** **High**. Verifies parsing correctness.
* **What it does:** Tests `RustParser` against both native and fallback modes, verifying function detection, line numbers, statements, and metric counts.
* **What it consists of:**
  - Unit tests for function signature extraction, statement splitting, and metric counters.

---

#### [`tests/test_graph.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_graph.py)
* **Usage:** Run via `pytest tests/test_graph.py`.
* **Importance:** **High**. Verifies graph topology algorithms.
* **What it does:** Tests `ASTGraphBuilder`, `CFGGraphBuilder`, `FLOGGraphBuilder`, and `CPGBuilder`. Verifies node/edge generation, cyclomatic complexity calculations, and cross-layer edge formation.
* **What it consists of:**
  - Unit tests asserting graph structure, edge types, and complexity bounds.

---

#### [`tests/test_outliers.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_outliers.py)
* **Usage:** Run via `pytest tests/test_outliers.py`.
* **Importance:** **High**. Validates structural anomaly detection.
* **What it does:** Verifies that `GraphOutlierAnalyzer` correctly identifies unsafe scopes, high complexity, clones, and heap allocations, mapping them to the proper CWE definitions.
* **What it consists of:**
  - Unit tests asserting outlier reporting on known vulnerable fixtures.

---

#### [`tests/test_metrics.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_metrics.py)
* **Usage:** Run via `pytest tests/test_metrics.py`.
* **Importance:** **High**. Validates the mathematical scoring integrity.
* **What it does:** Tests `QualityVectorCalculator` and `RQISynthesizer`. Asserts vector deductions for safety, performance, maintainability, and security, and checks non-linear penalty triggering.
* **What it consists of:**
  - Unit tests checking score ranges ($0 \le \text{score} \le 100$), weights, penalty applications, and letter grading.

---

#### [`tests/test_cwe.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_cwe.py)
* **Usage:** Run via `pytest tests/test_cwe.py`.
* **Importance:** **High**. Validates MITRE CWE catalog integrity.
* **What it does:** Ensures that all CWE entries in `CWERegistry` contain valid names, valid official MITRE URL schemes, categories, and severity levels. Tests tag creation and detection mappings.
* **What it consists of:**
  - Unit tests checking catalog schema, URL validity, and tag formatting.

---

#### [`tests/test_ai.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_ai.py)
* **Usage:** Run via `pytest tests/test_ai.py`.
* **Importance:** **High**. Verifies AI prompt generation and response parsing.
* **What it does:** Tests `XAIPromptBuilder` and `XAIEngine` using mock LLM responses. Verifies that prompt text includes deterministic graph facts and that patch extraction, explanation extraction, and diffing work reliably.
* **What it consists of:**
  - Unit tests with mock clients verifying prompt structure and diff generation without requiring live API keys.

---

#### [`tests/test_upload.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_upload.py)
* **Usage:** Run via `pytest tests/test_upload.py`.
* **Importance:** **High**. Validates file upload safety and HTTP behavior.
* **What it does:** Sends multipart file uploads to `/api/upload`. Verifies rejection of non-`.rs` extensions, empty files, and UTF-8 decoding errors.
* **What it consists of:**
  - HTTP integration tests for the upload endpoint.

---

#### [`tests/test_report.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_report.py)
* **Usage:** Run via `pytest tests/test_report.py`.
* **Importance:** **High**. Validates executive PDF document generation.
* **What it does:** Invokes `RustAuditPDFReportGenerator` and tests `/api/export/pdf`. Validates that generated PDF byte streams start with `%PDF-1.4`, contain all required sections, and handle single/multi-function payloads.
* **What it consists of:**
  - Unit and integration tests verifying PDF generation, header validation, and pagination.

---

#### [`tests/test_end_to_end.py`](file:///c:/Users/Admin/Desktop/Projects/RustAudit/tests/test_end_to_end.py)
* **Usage:** Run against a live running server:
  ```bash
  python tests/test_end_to_end.py
  ```
* **Importance:** **Critical**. Validates the entire integrated system end-to-end.
* **What it does:**
  1. Verifies the HTML dashboard template has all required controls.
  2. Uploads `tests/samples/sample_func.rs` via `/api/upload`.
  3. Simulates in-browser code editing by appending a custom subroutine.
  4. Triggers `/api/analyze` and validates all 3 functions, CPG graphs, RQI scores, cross-layer edges, and CWE summaries.
* **What it consists of:**
  - Comprehensive end-to-end verification script using standard library `urllib`.

---

## Filewise Project Execution Flow

This section details exactly **how execution control moves from one file to another** during different operational modes of RustAuditAI.

```
+----------------------------------------------------------------------------------------------------+
|                                      RUSTAUDIT AI EXECUTION FLOW                                   |
+----------------------------------------------------------------------------------------------------+

   [CLI INVOCATION]                                        [WEB / BROWSER INVOCATION]
      main.py                                                rustaudit/server.py
         │                                                            │
         │ (Reads target .rs)                                         │ (GET /)
         │                                                            ▼
         │                                                rustaudit/web/templates/index.html
         │                                                            │
         │                                                            │ (User clicks "Analyze")
         │                                                            ▼
         │                                                rustaudit/web/static/js/app.js
         │                                                            │
         │                                                            │ (POST /api/analyze)
         │                                                            ▼
         └─────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
                    rustaudit/parser/rust_parser.py
                                   │
                                   ├─► Subprocess to `cargo_parser/src/main.rs` (if built)
                                   │     (Reads AST via `syn` crate, returns JSON)
                                   │
                                   └─► Fallback: Python regex-AST parser
                                   │
                     Output: List[FunctionAstInfo]
                                   │
                                   ▼
                      rustaudit/graph/cpg_builder.py
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       ▼                           ▼                           ▼
rustaudit/graph/            rustaudit/graph/            rustaudit/graph/
  ast_graph.py                cfg_graph.py                flog_graph.py
(Builds AST nodes)         (Computes McCabe V(G))    (Tracks clones, allocs, unsafe)
       │                           │                           │
       └───────────────────────────┼───────────────────────────┘
                                   │
                        (Injects cross-layer edges)
                                   │
                        Output: CodePropertyGraph
                                   │
                                   ▼
                   rustaudit/graph/outlier_analyzer.py
                                   │ (Queries definitions)
                                   ▼
                      rustaudit/cwe/registry.py
                     (Maps to MITRE CWE catalog)
                                   │
                                   ▼
                 rustaudit/metrics/vector_calculators.py
                   (Computes Safety, Perf, Maint, Sec)
                                   │
                                   ▼
                  rustaudit/metrics/rqi_synthesizer.py
               (Applies non-linear penalties & computes RQI)
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │ (If explain requested)                            │ (If clean or explain=false)
         ▼                                                   ▼
rustaudit/ai/xai_engine.py                         Deliver Assessment Payload
         │                                                   │
         ├─► rustaudit/ai/prompt_builder.py                  ├─► CLI stdout (`main.py`)
         │     (Binds CPG facts & CWE tags)                  │
         │                                                   ├─► JSON response to `app.js`
         ├─► rustaudit/ai/llm_client.py                      │     (Renders Vis.js CPG & Gauges)
         │     (Calls Gemini / Groq API)                     │
         │                                                   └─► PDF Report Generation
         └─► Extract diff via `difflib`                            (rustaudit/reports/pdf_generator.py)
```

---

### Flow A: CLI Batch Execution Flow (`main.py`)

When a developer analyzes a Rust file from the command line:

```
Step 1: main.py
        User invokes `python main.py sample.rs --explain`.
        Reads raw file contents from `sample.rs`.
        Instantiates `RustParser()`, `CPGBuilder()`, `RQISynthesizer()`, and `XAIEngine()`.
           │
           ▼
Step 2: rustaudit/parser/rust_parser.py
        Calls `parser.parse_file("sample.rs")`.
        Spawns `cargo_parser/src/main.rs` (compiled binary) via subprocess.
        If binary is absent, executes `_python_fallback_parse()`.
        Produces a list of `FunctionAstInfo` objects, with line numbers resolved.
           │
           ▼
Step 3: rustaudit/graph/cpg_builder.py
        Loops over each `FunctionAstInfo`.
        Calls `ast_builder.build_ast_graph()` in `ast_graph.py` -> generates syntax tree.
        Calls `cfg_builder.build_cfg_graph()` in `cfg_graph.py` -> generates control flow and computes McCabe V(G).
        Calls `flog_builder.build_flog_graph()` in `flog_graph.py` -> maps borrows, clones, and unsafe operations.
        Merges nodes with `AST::`, `CFG::`, and `FLOG::` prefixes.
        Generates cross-layer linking edges (`AST_TO_CFG`, `AST_TO_FLOG`, `CFG_TO_FLOG_UNSAFE`, `CFG_TO_FLOG_BIND`).
        Produces unified `CodePropertyGraph`.
           │
           ▼
Step 4: rustaudit/metrics/rqi_synthesizer.py
        Calls `synthesizer.compute_rqi(fn, cpg)`.
        Hands control to `rustaudit/metrics/vector_calculators.py`.
           │
           ▼
Step 5: rustaudit/metrics/vector_calculators.py
        Queries `rustaudit/cwe/registry.py` for each detected pattern:
          - Unsafe function/blocks -> queries CWE-676, CWE-119.
          - Clones & allocations in loops -> queries CWE-400, CWE-770.
          - High cyclomatic complexity -> queries CWE-710.
          - Unchecked .unwrap() or direct indexing -> queries CWE-252, CWE-129.
        Returns `VectorScores` with exact deduction points and statement line numbers.
           │
           ▼
Step 6: rustaudit/metrics/rqi_synthesizer.py
        Computes weighted sum:
        RQI = 0.30*Safety + 0.25*Perf + 0.25*Maint + 0.20*Security.
        Evaluates dynamic non-linear penalties (e.g. Safety < 60 triggers 15% reduction).
        Assigns letter grade (e.g. "C (Needs Refactoring)").
        Returns `RQISummary`.
           │
           ▼
Step 7: rustaudit/ai/xai_engine.py (Triggered if `--explain` was passed)
        If score is already 100%, generates a clean compliance summary and returns.
        Otherwise:
          1. Calls `rustaudit/ai/prompt_builder.py` to construct a deterministic prompt containing CPG facts and CWE tags.
          2. Calls `rustaudit/ai/llm_client.py` to dispatch REST request to Google Gemini (or Groq fallback).
          3. Extracts refactored Rust code block from response.
          4. Computes unified diff using Python's `difflib`.
          5. Returns `XAIReport`.
           │
           ▼
Step 8: main.py
        Formats assessment report to console with RQI score, active penalties, line-specific deductions, and the refactored code patch.
```

---

### Flow B: Web UI & REST API Execution Flow (`server.py`)

When a developer interacts with the web application:

```
Step 1: rustaudit/server.py
        Server is started via `python rustaudit/server.py`.
        FastAPI initializes instances of `RustParser`, `CPGBuilder`, `GraphOutlierAnalyzer`, `RQISynthesizer`, `XAIEngine`, and `RustAuditPDFReportGenerator`.
        Mounts `/static` from `rustaudit/web/static`.
           │
           ▼
Step 2: Browser loads `GET /`
        `server.py` reads `rustaudit/web/templates/index.html` and returns it.
        Browser fetches `rustaudit/web/static/css/style.css` and `rustaudit/web/static/js/app.js`.
           │
           ▼
Step 3: File Upload (Optional: `POST /api/upload`)
        User drags a `.rs` file onto the drop overlay or clicks "Upload File".
        `app.js` sends multipart form-data to `server.py:upload_file()`.
        `server.py` checks `.rs` extension and decodes UTF-8 text.
        Returns code JSON to `app.js`, which populates `#code-editor`.
           │
           ▼
Step 4: Analysis Trigger (`POST /api/analyze`)
        User clicks "Analyze Code".
        `app.js` reads code from `#code-editor`, checks `#enable-xai-toggle`, and sends JSON payload `{"code": "...", "explain": true/false}` to `/api/analyze`.
           │
           ▼
Step 5: Execution in `rustaudit/server.py`
        1. Calls `parser.parse_code(req.code)` in `rustaudit/parser/rust_parser.py`.
        2. For each parsed function:
           a. Calls `builder.build_cpg(fn)` in `rustaudit/graph/cpg_builder.py` (which orchestrates `ast_graph.py`, `cfg_graph.py`, `flog_graph.py`).
           b. Calls `outlier_analyzer.analyze_outliers(fn, cpg)` in `rustaudit/graph/outlier_analyzer.py` (tags graph anomalies with CWEs from `cwe/registry.py`).
           c. Calls `synthesizer.compute_rqi(fn, cpg)` in `rustaudit/metrics/rqi_synthesizer.py` (scores vectors via `vector_calculators.py`).
           d. If `req.explain` is True:
              Calls `ai_engine.generate_explanation(fn, cpg, rqi_summary, fn_code)` in `rustaudit/ai/xai_engine.py` (via `prompt_builder.py` and `llm_client.py`).
        3. Formats response payload containing function summaries, full graph node/edge lists for AST/CFG/FLOG/CPG, RQI scores, deductions, and XAI patches.
           │
           ▼
Step 6: Rendering in `rustaudit/web/static/js/app.js`
        1. Hides loading state, displays `#audit-results-container`.
        2. Renders function tabs if multiple subroutines exist.
        3. Animates SVG circle gauge to the calculated RQI score and updates grade badge.
        4. Updates vector progress bars (Safety, Perf, Maint, Sec).
        5. Populates MITRE CWE counters and detailed deduction cards with clickable line navigation.
        6. Feeds nodes and edges into Vis.js Network canvas to render interactive graph models.
        7. If XAI was enabled, renders colored diffs and displays the complete idiomatic refactored code patch.
```

---

### Flow C: Executive PDF Report Generation Flow

When a user exports an audit report:

```
Step 1: User clicks "Export PDF Report" in the web dashboard.
           │
           ▼
Step 2: rustaudit/web/static/js/app.js
        Gathers active function audit data and dispatches `POST /api/export/pdf` with the audit payload.
           │
           ▼
Step 3: rustaudit/server.py
        Endpoint `export_pdf_report()` receives `ExportReportRequest`.
        Calls `generate_pdf_report()` in `rustaudit/reports/pdf_generator.py`.
           │
           ▼
Step 4: rustaudit/reports/pdf_generator.py
        Instantiates `RustAuditPDFReportGenerator`.
        Builds ReportLab story flow:
          - Generates branding header banner.
          - Renders executive RQI scorecard and vector weights table.
          - Renders MITRE CWE weakness counter strip.
          - Loops through structured deductions, formatting severity badges, statement code snippets, and remediation guidelines.
          - Renders Code Property Graph topology metrics.
          - Renders XAI root-cause findings and code patches (if present).
        Compiles document using two-pass `NumberedCanvas` to stamp running headers and "Page X of Y" footers.
        Returns raw PDF bytes.
           │
           ▼
Step 5: rustaudit/server.py
        Returns `Response` with `content_type="application/pdf"` and `Content-Disposition: attachment; filename="rustaudit_report_<fn>.pdf"`.
           │
           ▼
Step 6: Browser
        Downloads and opens the executive PDF report.
```

---

### Flow D: End-to-End Automated Test Flow

When running test verification:

```
Step 1: Developer runs `python tests/test_end_to_end.py`.
           │
           ▼
Step 2: tests/test_end_to_end.py
        Connects via HTTP to `http://127.0.0.1:8000/`.
        Verifies `index.html` serves all required DOM elements.
           │
           ▼
Step 3: tests/test_end_to_end.py -> tests/samples/sample_func.rs
        Reads sample Rust code.
        Uploads file to `/api/upload` (testing `server.py`).
        Simulates code modification in-memory.
           │
           ▼
Step 4: tests/test_end_to_end.py -> POST /api/analyze
        Executes full pipeline across multiple functions.
        Asserts:
          - AST, CFG, FLOG, and Unified CPG node and edge consistency.
          - Detection of cross-layer semantic edges (`AST_TO_CFG`, `AST_TO_FLOG`, `CFG_TO_FLOG`).
          - RQI score computation and non-linear penalties.
        Outputs passing test verdict.
```

---

## Cross-Module Dependency Matrix

The following table summarizes how each module in the project depends on other components:

| Module / File | Direct Dependencies | Depended Upon By |
| :--- | :--- | :--- |
| `main.py` | `RustParser`, `CPGBuilder`, `RQISynthesizer`, `XAIEngine` | End User CLI |
| `cargo_parser/src/main.rs` | `syn`, `quote`, `proc-macro2`, `serde`, `serde_json` | `rust_parser.py` (via subprocess) |
| `rustaudit/server.py` | `RustParser`, `CPGBuilder`, `GraphOutlierAnalyzer`, `RQISynthesizer`, `XAIEngine`, `pdf_generator`, FastAPI | Web Clients, `test_end_to_end.py` |
| `rustaudit/parser/rust_parser.py` | `cargo_parser` binary, Python standard library | `main.py`, `server.py`, `tests/` |
| `rustaudit/graph/ast_graph.py` | `networkx`, `FunctionAstInfo` | `cpg_builder.py` |
| `rustaudit/graph/cfg_graph.py` | `networkx`, `FunctionAstInfo` | `cpg_builder.py` |
| `rustaudit/graph/flog_graph.py` | `networkx`, `FunctionAstInfo` | `cpg_builder.py` |
| `rustaudit/graph/cpg_builder.py` | `ast_graph`, `cfg_graph`, `flog_graph`, `networkx` | `main.py`, `server.py`, `tests/` |
| `rustaudit/graph/outlier_analyzer.py` | `cpg_builder`, `cwe/registry.py` | `server.py`, `tests/` |
| `rustaudit/cwe/registry.py` | Python standard library | `vector_calculators.py`, `outlier_analyzer.py`, `prompt_builder.py`, `pdf_generator.py` |
| `rustaudit/metrics/vector_calculators.py` | `cpg_builder`, `cwe/registry.py` | `rqi_synthesizer.py` |
| `rustaudit/metrics/rqi_synthesizer.py` | `vector_calculators.py` | `main.py`, `server.py`, `xai_engine.py`, `tests/` |
| `rustaudit/ai/llm_client.py` | `httpx`, `python-dotenv` | `xai_engine.py` |
| `rustaudit/ai/prompt_builder.py` | `cpg_builder`, `rqi_synthesizer` | `xai_engine.py` |
| `rustaudit/ai/xai_engine.py` | `prompt_builder.py`, `llm_client.py`, `difflib` | `main.py`, `server.py`, `tests/` |
| `rustaudit/reports/pdf_generator.py` | `reportlab`, `cwe/registry.py` | `server.py`, `tests/` |
| `rustaudit/web/static/js/app.js` | Vis.js (CDN), `/api/upload`, `/api/analyze`, `/api/export/pdf` | `index.html` |

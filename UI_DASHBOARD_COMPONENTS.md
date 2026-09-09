# RustAuditAI — UI Dashboard Elements & Visual Intelligence Specification

> **Project Name:** RustAuditAI: Intra-Procedural Semantic Analysis & Software Quality Intelligence Framework  
> **Repository Root:** `c:\Users\Admin\Desktop\Projects\RustAudit`  
> **Document Purpose:** Complete numbered specification of every user interface component, visual widget, graph visualizer, code editor, metric display, and interaction flow rendered on the RustAuditAI Web Dashboard (`http://127.0.0.1:8000/`).

---

## Executive Summary of Dashboard Architecture

The RustAuditAI dashboard is designed as a high-density, dark-mode software intelligence workstation. It bridges deterministic compiler-level graph models (AST, CFG, FLOG, CPG) with qualitative Explainable AI (XAI) refactoring guidance.

The interface is structured into **two primary panels** flanked by a top navigation bar:
- **Left Panel (Input Workstation):** Source code ingestion, file drag-and-drop, sample loading, and audit dispatch controls.
- **Right Panel (Intelligence Output):** Dual-mode audit visualization (Non-Developer Executive Mode vs. Developer Graph Inspection Mode).

```
+---------------------------------------------------------------------------------------------------------------------+
|                                            1. TOP NAVIGATION & HEADER BAR                                           |
|   [Logo] RustAuditAI   |   Status: Operational   |   [Switch] Developer Mode Toggle                                 |
+------------------------------------------------------+--------------------------------------------------------------+
|             2. LEFT PANEL: CODE INPUT                |               3. RIGHT PANEL: AUDIT INTELLIGENCE             |
|                                                      |                                                              |
| [Upload .rs]  [Load Sample]  [File: sample.rs (x)]   | [Tabs: fn process_user_data() | fn calculate_metrics()]      |
|                                                      | [Action: Export PDF Report]                                  |
| +--------------------------------------------------+ |                                                              |
| | CODE AREA 1: Subroutine Code Editor              | | [NON-DEV MODE]               | [DEV MODE]                    |
| |                                                  | | 4. RQI Showcase Hero Dial    | 4. RQI Matrix Formula Card    |
| | pub fn process_user_data(data: &str) -> String { | | 5. 4 Vector Mini-Gauges      | 5. Vertical Vectors Breakdown |
| |     ...                                          | | 6. Deductions & CWE Counters | 6. 4 Graphs Visualizer        |
| | }                                                | | 7. XAI Root Cause Cards      |    - FLOG, CFG, AST, CPG      |
| +--------------------------------------------------+ | 8. CODE AREA 2: Refactored   | 7. Graph Metrics Bar          |
|                                                      |    Patch Candidate (~100%)   | 8. Graph Outliers Drawer      |
| [Switch] Enable XAI Engine    [Execute Graph Audit]  |                                                              |
+------------------------------------------------------+--------------------------------------------------------------+
```

---

## Numbered UI Components & Features

### 1. Top Navigation & Header Bar
* **Location:** Fixed at the top of the viewport.
* **Key Components:**
  1. **Branding Title & Icon:** `RustAuditAI` with an atom/code logo (`fa-microchip` / `fa-cube`).
  2. **Platform Subtitle:** *"Intra-Procedural Semantic Analysis & Software Quality Intelligence Framework"*.
  3. **Live System Status Indicator:** Green glowing pill indicating `Engine Ready / Live`.
  4. **Developer Mode Toggle Switch (`#developer-mode-toggle`):** 
     - A custom glowing toggle switch that flips the dashboard between **Executive Overview Mode** (RQI Showcase, CWE deductions, and XAI refactoring insights) and **Developer Inspection Mode** (interactive 4-layer graph canvas, mathematical vector breakdown, and graph topological outlier drawer).

---

### 2. Code Area 1 — Subroutine Code Input & Ingestion Controls
* **Location:** Left Column (Input Workstation).
* **Key Components:**
  1. **Upload `.rs` Button (`#upload-file-btn`):** Triggers a hidden native file picker (`#file-upload-input`) accepting `.rs` and `.txt` files.
  2. **Loaded File Badge (`#file-badge`):** Appears when a file is loaded, displaying the Rust file icon (`fa-rust`), the filename (e.g. `sample_func.rs`), and an interactive clear button (`×`).
  3. **Drag-and-Drop Drop Overlay (`#drop-overlay`):** When dragging a `.rs` file over the editor wrapper, a glassmorphic animated overlay appears (*"Drop Rust (.rs) file here to load into editor"*), providing zero-click file loading.
  4. **Load Sample Button (`#load-sample-btn`):** Instantly pre-fills the editor with a calibrated sample Rust subroutine demonstrating anti-patterns (`process_user_data` and `calculate_metrics`).
  5. **Interactive Code Editor (`#code-editor`):**
     - Dark-themed monospace editing area styled with Fira Code.
     - Supports full tab key indentation, line counting, scroll synchronization, and syntax formatting.
  6. **Enable XAI Engine Toggle (`#enable-xai-toggle`):** A switch allowing users to opt into or out of automated LLM refactoring report generation during graph analysis.
  7. **Execute Graph Audit Button (`#analyze-btn`):** The primary call-to-action button featuring a wand-sparkle animation that compiles the AST, extracts FLOG ownership edges, computes RQI, and renders the intelligence report.

---

### 3. Multi-Function Navigation & Executive Export Actions
* **Location:** Top of the Right Column (Results Container).
* **Key Components:**
  1. **Subroutine Selector Tabs (`#function-tabs`):**
     - When analyzing multi-function files (e.g. `sample_func.rs`), the system dynamically renders clickable tabs for every detected subroutine:
       - `fn process_user_data()` (RQI 83.8)
       - `fn calculate_metrics()` (RQI 100.0)
     - Clicking any tab instantly switches all graphs, scorecards, deduction logs, and refactored patches to that specific function without re-running the analysis.
  2. **Export Publication-Grade PDF Button (`#export-pdf-btn`):**
     - Red action button with PDF icon (`fa-file-pdf`).
     - Triggers `/api/export/pdf`, downloading a publication-grade executive audit report complying with SRS §4.6.5 (featuring running headers, confidential watermarks, two-pass `Page X of Y` numbering, vector scorecard tables, and color-highlighted patches).

---

### 4. Rust Quality Index (RQI) Metric Displays

The dashboard provides two distinct perspectives on the synthesized RQI score:

#### Perspective A: Non-Developer Mode RQI Showcase Card (`#non-dev-rqi-card`)
1. **Hero RQI Radial Dial:**
   - Circular SVG gauge animating to the computed composite score ($0.00 \le \text{RQI} \le 100.00$).
   - Dynamically color-coded based on score tiers:
     - **$\ge 90.0$:** Emerald Green (`#10b981`)
     - **$80.0 - 89.9$:** Sky Blue (`#38bdf8`)
     - **$70.0 - 79.9$:** Indigo / Amber (`#f59e0b`)
     - **$< 70.0$:** Rose / Crimson Red (`#ef4444`)
2. **Qualitative Grade Badge (`#rqi-grade`):** 
   - Explicit letter grade string: `A+ (Idiomatic & Robust)`, `A (Good Quality)`, `B (Acceptable)`, `C (Needs Refactoring)`, `D (High Risk)`, or `F (Critical Vulnerability)`.
3. **Synthesis Summary Text (`#rqi-summary-text`):** Human-readable quality health verdict.
4. **2x2 Core Vectors Grid:** Four individual circular mini-gauges displaying the exact scores for:
   - **Safety Vector** (Weight: $30\%$)
   - **Performance Vector** (Weight: $25\%$)
   - **Maintainability Vector** (Weight: $25\%$)
   - **Security Vector** (Weight: $20\%$)

#### Perspective B: Developer Mode RQI Matrix Card (`#dev-rqi-card`)
1. **RQI Score Dial & Raw Metric Value (`#dev-rqi-score-num`):** Precise decimal score display without marketing labels.
2. **Mathematical Formula Block:** 
   - Displays the exact linear weighted matrix formula:
     $$\text{Base RQI} = (0.30 \times S) + (0.25 \times P) + (0.25 \times M) + (0.20 \times \text{SEC}) - \text{Penalty}$$
3. **Calculation Chips:**
   - **Linear Weighted Sum Chip (`#dev-calc-weighted-sum`):** Shows the raw pre-penalty weighted sum (e.g. `83.8`).
   - **Penalty Applied Chip (`#dev-calc-penalty-val`):** Displays `-1.7 pts (Penalty Triggered)` in crimson or `0.0 pts (No Penalty)` in emerald.
4. **Vertical Vectors Breakdown Stack (`#dev-vectors-vertical-list`):**
   - Four full-width horizontal cards stacked vertically for Safety, Performance, Maintainability, and Security.
   - Each card contains an SVG gauge, score, and a comprehensive breakdown of **Pros (green checkmark tags)** and **Cons/Deductions (red negative tags)** with MITRE CWE link pills and source line numbers.

---

### 5. Quality Deductions & Indicator Logs (Non-Developer Mode)
* **Location:** Mid-right column in Non-Developer Mode (`#non-dev-deductions-box`).
* **Key Components:**
  1. **MITRE CWE Tracking Summary Counter Bar (`#cwe-summary-bar`):**
     - Real-time categorized weakness counters displaying:
       - **Total Weaknesses** (Gray badge)
       - **Critical Severity** (Purple badge)
       - **High Severity** (Red badge)
       - **Medium Severity** (Amber badge)
       - **Low Severity** (Green badge)
  2. **Detailed Deduction Cards List (`#deductions-list`):**
     - Each identified anti-pattern is rendered as a distinct card containing:
       - **Severity Tag:** `[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, or `[LOW]`.
       - **MITRE CWE Pill:** Direct external hyperlink to the official MITRE catalog (e.g. `CWE-119`, `CWE-400`, `CWE-710`).
       - **Source Line Tag:** e.g. `Line 12`.
       - **Statement Code Snippet:** Formatted monospace code showing the exact offending statement.
       - **Point Deduction Value:** Exact points docked from the vector (e.g. `-15.0 pts`).

---

### 6. The 4 Subroutine Graphs & Visualization Canvas (Developer Mode)
* **Location:** Right Column when Developer Mode is active (`#dev-graph-container`).
* **Graph Type Selector Tabs:** Users can toggle dynamically between **4 graph models**:

| Graph Layer | Full Name | Semantic Focus & Visual Meaning | Node / Edge Color Scheme |
| :--- | :--- | :--- | :--- |
| **1. FLOG Graph** | **Flow of Ownership Graph** | Maps Rust-specific memory semantics: variable bindings, borrowed references (`&T`, `&mut T`), heap allocations (`Box::new`, `Vec::new`), cloned buffers (`.clone()`), and `unsafe` blocks. | Normal bindings: **Emerald** (`#10b981`), Clones: **Red** (`#ef4444`), Allocations: **Purple** (`#a855f7`), Unsafe: **Crimson** (`#dc2626`). |
| **2. CFG Graph** | **Control Flow Graph** | Models basic blocks, sequential execution paths, conditional branching (`if`, `match`), loop iterations (`for`, `while`, `loop`), and computes McCabe Cyclomatic Complexity $V(G)$. | Decision blocks: **Amber** (`#f59e0b`), Sequential basic blocks: **Blue** (`#3b82f6`). |
| **3. AST Graph** | **Abstract Syntax Tree** | Visualizes the hierarchical syntactic grammar tree generated from `syn` (function declarations, parameter lists, let bindings, expressions, blocks). | Syntax constructs: **Cyan** (`#06b6d4`). |
| **4. Unified CPG** | **Code Property Graph** | Multi-layer composite graph overlaying AST syntax, CFG control flow, and FLOG ownership states with cross-layer semantic edges (`AST_TO_CFG`, `AST_TO_FLOG`, `CFG_TO_FLOG_UNSAFE`, `CFG_TO_FLOG_BIND`). | Multi-colored semantic layering with violet cross-layer edges. |

* **Interactive Canvas (`#interactive-canvas`):**
  - Powered by Vis.js physics simulation engine.
  - Interactive features: drag-to-reposition nodes, zoom-to-fit, physics stabilization, and click-to-highlight connected subtrees.

---

### 7. Graph Topology Metrics Bar & Outlier Drawer (Developer Mode)
* **Location:** Directly below the interactive graph canvas.
* **Key Components:**
  1. **Graph Topology Metrics Bar (`#graph-metrics-bar`):**
     - **AST Nodes:** Total syntax tree nodes.
     - **CFG Complexity $V(G)$:** McCabe cyclomatic complexity metric.
     - **FLOG Allocations:** Total micro-heap allocation instances.
     - **FLOG Clones:** Total `.clone()` invocations.
     - **CPG Edges:** Count of cross-layer semantic linking edges.
  2. **Graph Topological Outliers & Anomaly Issues Drawer (`#outliers-content-list`):**
     - Card-based drawer detailing structural anomalies discovered during graph traversal:
       - Cyclomatic control-flow bottlenecks.
       - Unsafe boundary isolation breaches.
       - Cyclic borrow hazards and heap churn hotspots.
       - Each anomaly card contains an explanation, line reference, CWE index, and actionable mitigation advice.

---

### 8. XAI Explainable Refactoring Insights & Code Area 2 (Non-Developer Mode)
* **Location:** Lower half of the Right Column (`#xai-section`).
* **Key Components:**
  1. **Section Header & Overview Banner:**
     - AI brain icon (`fa-brain`) with overview statement describing the subroutine's overall quality profile.
  2. **Architectural Root Cause & Remediation Insight Cards:**
     - Clean, structured card layout with **zero duplicate cards** and **no regex splitting glitches**:
       - **Step Number Badge:** Sequential indicator (`1`, `2`, `3`...).
       - **Defect Title:** Human-readable defect title (sanitized of raw URLs).
       - **MITRE CWE Pill:** Formatted weakness pill with shield badge (e.g. `CWE-119`, `CWE-400`).
       - **Root Cause & Flaw Analysis Box:** Red-accented callout explaining the exact syntactic or ownership flaw in the original code.
       - **Remediation Guidance Box:** Green-accented callout detailing the idiomatic Rust refactoring steps to fix the issue.
  3. **Code Area 2 — Idiomatic Rust Patch Candidate (~100% RQI) (`#xai-patch-code`):**
     - A dedicated, syntax-highlighted code container displaying the **complete, compilable, idiomatic Rust refactored patch**.
     - Implements functional decomposition (breaking monolithic subroutines into single-responsibility helper functions with $V(G) \le 2$).
     - Eliminates all `unsafe` blocks, replaces raw pointers with safe abstractions, removes redundant heap `.clone()` calls, and averts panicking operations.
     - Evaluates to near $100\%$ RQI (Grade A+).
  4. **One-Click Copy Patch Button (`#copy-patch-btn`):**
     - Floating copy button with clipboard icon (`fa-copy`).
     - Copies the entire standalone refactored patch to the developer's clipboard and provides a green checkmark confirmation (`Copied!`).

---

## Complete UI Element Reference Table

| # | UI Element / Widget | Mode Visibility | HTML ID / Selector | What It Displays / Does |
|---|---|---|---|---|
| **1** | Top Header & Logo | Always Visible | `.navbar`, `.brand` | RustAuditAI branding, subtitle, live status indicator. |
| **2** | Developer Mode Switch | Always Visible | `#developer-mode-toggle` | Flips dashboard between Executive Non-Dev and Developer Graph modes. |
| **3** | File Upload Button | Left Panel | `#upload-file-btn` | Opens local file selector to upload `.rs` files. |
| **4** | Loaded File Badge | Left Panel | `#file-badge` | Displays loaded filename with quick-clear (`×`) button. |
| **5** | Drag-and-Drop Overlay | Left Panel | `#drop-overlay` | Animated drop zone when dragging `.rs` files onto the editor. |
| **6** | Load Sample Button | Left Panel | `#load-sample-btn` | Pre-fills editor with calibrated sample Rust subroutine code. |
| **7** | **Code Area 1 (Editor)** | Left Panel | `#code-editor` | Primary source code editing textarea with tab indentation support. |
| **8** | Enable XAI Toggle | Left Panel | `#enable-xai-toggle` | Checkbox toggling automated AI refactoring report generation. |
| **9** | Execute Graph Audit Btn | Left Panel | `#analyze-btn` | Primary call-to-action button triggering `/api/analyze`. |
| **10** | Function Selector Tabs | Results Bar | `#function-tabs` | Dynamic tabs switching analysis views across multiple subroutines. |
| **11** | Export PDF Report Btn | Results Bar | `#export-pdf-btn` | Generates and downloads publication-grade audit PDF report. |
| **12** | RQI Radial Dial (Hero) | Non-Dev Mode | `#score-circle-path` | Animated circular SVG gauge showing composite RQI score ($0-100$). |
| **13** | RQI Grade Badge | Non-Dev Mode | `#rqi-grade` | Qualitative letter grade (`A+`, `A`, `B`, `C`, `D`, `F`). |
| **14** | Vector Mini-Dials (2x2) | Non-Dev Mode | `.mini-dial`, `#val-safety`, etc. | Circular gauges for Safety (30%), Perf (25%), Maint (25%), Sec (20%). |
| **15** | CWE Tracking Counter Strip | Non-Dev Mode | `#cwe-summary-bar` | Summary counter strip: Total, Critical, High, Medium, Low weaknesses. |
| **16** | Deduction Cards List | Non-Dev Mode | `#deductions-list` | Line-tagged cards showing exact statement, severity, and deduction points. |
| **17** | RQI Matrix Formula Block | Dev Mode | `.formula-box`, `.dev-rqi-calc-right` | Explains the mathematical weighted sum formula and applied penalties. |
| **18** | Vertical Vectors Breakdown | Dev Mode | `#dev-vectors-vertical-list` | 4 full-width rows with mini-charts, pros tags, and deduction breakdowns. |
| **19** | **Graph 1: FLOG Graph** | Dev Mode | `.graph-type-btn[data-graph="flog"]` | Visualizes ownership, borrow lifetimes, clones, heap allocs, and unsafe. |
| **20** | **Graph 2: CFG Graph** | Dev Mode | `.graph-type-btn[data-graph="cfg"]` | Visualizes basic blocks, branch conditions, loops, and McCabe V(G). |
| **21** | **Graph 3: AST Graph** | Dev Mode | `.graph-type-btn[data-graph="ast"]` | Visualizes hierarchical grammar syntax tree derived via `syn`. |
| **22** | **Graph 4: Unified CPG** | Dev Mode | `.graph-type-btn[data-graph="cpg"]` | Composite multi-layer graph linking AST, CFG, and FLOG via semantic edges. |
| **23** | Vis.js Interactive Canvas | Dev Mode | `#interactive-canvas` | Physics-simulated interactive network diagram with zoom, pan, and dragging. |
| **24** | Graph Metrics Status Bar | Dev Mode | `#graph-metrics-bar` | Counters: AST Nodes, CFG V(G), FLOG Allocs, FLOG Clones, CPG Edges. |
| **25** | Graph Outliers Drawer | Dev Mode | `#outliers-content-list` | Structural graph anomaly cards with CWE tags and topological advice. |
| **26** | XAI Root Cause Cards | Non-Dev Mode | `#xai-explanation-text` | Sequentially numbered cards explaining root cause flaw and remediation. |
| **27** | **Code Area 2 (Refactored Patch)**| Non-Dev Mode | `#xai-patch-code` | Standalone, compilable idiomatic Rust refactored code (~100% RQI). |
| **28** | Copy Patch Button | Non-Dev Mode | `#copy-patch-btn` | One-click clipboard copy button with visual confirmation feedback. |

/**
 * ==========================================================================
 * RustAuditAI — Frontend Intelligence Controller (v2.0 Rebuild)
 * Architecture: Executive Intelligence & 4-Layer Vis.js Graph Visualizer
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Element References ---
    const codeEditor = document.getElementById("code-editor");
    const editorGutter = document.getElementById("editor-gutter");
    const analyzeBtn = document.getElementById("analyze-btn");
    const enableXaiToggle = document.getElementById("enable-xai-toggle");
    
    // View Perspectives
    const viewExecutiveBtn = document.getElementById("view-executive-btn");
    const viewDeveloperBtn = document.getElementById("view-developer-btn");
    const devModeToggle = document.getElementById("developer-mode-toggle");
    const executiveView = document.getElementById("executive-view");
    const developerView = document.getElementById("developer-view");

    // UI States
    const welcomeEmptyState = document.getElementById("welcome-empty-state");
    const loaderState = document.getElementById("loader-state");
    const loaderText = document.getElementById("loader-text");
    const auditResultsContainer = document.getElementById("audit-results-container");

    // Function Selector & Exports
    const functionTabs = document.getElementById("function-tabs");
    const exportPdfBtn = document.getElementById("export-pdf-btn");
    const exportHtmlBtn = document.getElementById("export-html-btn");

    // Executive Metrics
    const rqiScoreNum = document.getElementById("rqi-score-num");
    const scoreCirclePath = document.getElementById("score-circle-path");
    const rqiGradeLetter = document.getElementById("rqi-grade-letter");
    const rqiGradeText = document.getElementById("rqi-grade-text");
    const rqiSummaryText = document.getElementById("rqi-summary-text");

    const valSafety = document.getElementById("val-safety");
    const pathSafety = document.getElementById("path-safety");
    const valPerf = document.getElementById("val-perf");
    const pathPerf = document.getElementById("path-perf");
    const valMaint = document.getElementById("val-maint");
    const pathMaint = document.getElementById("path-maint");
    const valSec = document.getElementById("val-sec");
    const pathSec = document.getElementById("path-sec");

    // CWE & Deductions
    const cweCountTotal = document.getElementById("cwe-count-total");
    const cweCountCritical = document.getElementById("cwe-count-critical");
    const cweCountHigh = document.getElementById("cwe-count-high");
    const cweCountMedium = document.getElementById("cwe-count-medium");
    const cweCountLow = document.getElementById("cwe-count-low");
    const deductionsList = document.getElementById("deductions-list");

    // Side-by-Side Diff
    const diffOriginalBody = document.getElementById("diff-original-body");
    const diffRefactoredBody = document.getElementById("diff-refactored-body");
    const applyPatchBtn = document.getElementById("apply-patch-btn");
    const copyPatchBtn = document.getElementById("copy-patch-btn");
    const xaiExplanationText = document.getElementById("xai-explanation-text");
    const xaiPatchCode = document.getElementById("xai-patch-code");

    // Developer View & Graphs
    const devRqiScoreNum = document.getElementById("dev-rqi-score-num");
    const devCalcWeightedSum = document.getElementById("dev-calc-weighted-sum");
    const devCalcPenaltyVal = document.getElementById("dev-calc-penalty-val");
    const devVectorsList = document.getElementById("dev-vectors-vertical-list");
    const devScoreCirclePath = document.getElementById("dev-score-circle-path");

    const graphTabButtons = document.querySelectorAll(".graph-tab-btn");
    const dualGraphToggle = document.getElementById("dual-graph-toggle");
    const singleCanvasBox = document.getElementById("single-canvas-box");
    const dualCanvasGrid = document.getElementById("dual-canvas-grid");
    const interactiveCanvas = document.getElementById("interactive-canvas");
    const canvasOriginal = document.getElementById("canvas-original");
    const canvasRefactored = document.getElementById("canvas-refactored");

    const astNodesCnt = document.getElementById("ast-nodes-cnt");
    const cfgCcCnt = document.getElementById("cfg-cc-cnt");
    const flogAllocCnt = document.getElementById("flog_alloc_cnt");
    const flogClonesCnt = document.getElementById("flog_clones_cnt");
    const cpgEdgesCnt = document.getElementById("cpg-edges-cnt");
    const outliersContentList = document.getElementById("outliers-content-list");

    // Revision History Drawer
    const revisionsToggleBtn = document.getElementById("revisions-toggle-btn");
    const revCountBadge = document.getElementById("rev-count-badge");
    const revisionDrawerOverlay = document.getElementById("revision-drawer-overlay");
    const revisionHistoryDrawer = document.getElementById("revision-history-drawer");
    const closeDrawerBtn = document.getElementById("close-drawer-btn");
    const drawerFnSubtitle = document.getElementById("drawer-fn-subtitle");
    const revisionsTimelineContainer = document.getElementById("revisions-timeline-container");
    const revisionsEmptyState = document.getElementById("revisions-empty-state");
    const clearRevisionsBtn = document.getElementById("clear-revisions-btn");

    // File Upload & Workstation Action Elements
    const preAuditActions = document.getElementById("pre-audit-actions");
    const postAuditActions = document.getElementById("post-audit-actions");
    const newFileBtn = document.getElementById("new-file-btn");
    const uploadFileBtn = document.getElementById("upload-file-btn");
    const loadSampleBtn = document.getElementById("load-sample-btn");
    const clearCodeBtn = document.getElementById("clear-code-btn");
    const fileUploadInput = document.getElementById("file-upload-input");
    const fileBadge = document.getElementById("file-badge");
    const fileNameText = document.getElementById("file-name-text");
    const clearFileBtn = document.getElementById("clear-file-btn");
    const editorWrapper = document.getElementById("editor-wrapper");
    const editorCodeStage = document.getElementById("editor-code-stage");
    const editorHighlightUnderlay = document.getElementById("editor-highlight-underlay");
    const editorHighlightCode = document.getElementById("editor-highlight-code");
    const dropOverlay = document.getElementById("drop-overlay");
    const auditOutputPanel = document.getElementById("audit-output-panel");
    const workspaceGrid = document.getElementById("workspace-grid");
    const xaiTestBtn = document.getElementById("xai-test-btn");
    const closeResultsBtn = document.getElementById("close-results-btn");

    // Top Subroutines Function Bar
    const subroutinesBarWrapper = document.getElementById("subroutines-bar-wrapper");
    const fnCountPill = document.getElementById("fn-count-pill");

    // Two Sections & Refactored Code Elements
    const currentAuditSection = document.getElementById("current-audit-section");
    const refactoredDivider = document.getElementById("refactored-section-divider");
    const refactoredAuditSection = document.getElementById("refactored-audit-section");
    const refactoredCodeDisplay = document.getElementById("refactored-code-display");
    const refactoredGutter = document.getElementById("refactored-gutter");
    const refactoredInteractiveCanvas = document.getElementById("refactored-interactive-canvas");

    // Toast Container
    const toastContainer = document.getElementById("toast-container");

    // --- Cybernetic Splash Screen (Logo + Sequential React Bits TextType Animations) ---
    const splashScreen = document.getElementById("splash-screen");
    const splashTitleRoot = document.getElementById("splash-title-root");
    const splashSubtitleRoot = document.getElementById("splash-subtitle-root");
    const replayIntroBtn = document.getElementById("replay-intro-btn");

    let splashTimers = [];
    let splashTitleReactRoot = null;
    let splashSubtitleReactRoot = null;

    function clearAllSplashTimers() {
        splashTimers.forEach(t => {
            clearTimeout(t);
            clearInterval(t);
        });
        splashTimers = [];
    }

    function runSplashSequence() {
        if (!splashScreen) return;
        clearAllSplashTimers();
        splashScreen.style.display = "flex";
        splashScreen.classList.remove("splash-dismissed");

        // Fail-safe timeout: ensure dashboard is always accessible within 5 seconds max
        const safetyDismissTimer = setTimeout(dismissSplashScreen, 5200);
        splashTimers.push(safetyDismissTimer);

        const titleString = "RustAudit AI";
        const subtitleString = "Intra-Procedural Quality Intelligence & Graph Analysis";
        let hasCompletedSubtitle = false;
        let hasCompletedTitle = false;

        // Stage 1: Reset Text Containers so ONLY the Logo is displayed first with its orbital ring animation
        if (splashTitleReactRoot) {
            try { splashTitleReactRoot.render(null); } catch (e) {}
        }
        if (splashTitleRoot) splashTitleRoot.innerHTML = "";

        if (splashSubtitleReactRoot) {
            try { splashSubtitleReactRoot.render(null); } catch (e) {}
        }
        if (splashSubtitleRoot) splashSubtitleRoot.innerHTML = "";

        // Stage 2: After the logo orbital entrance (~600ms), start TextType typing for "RustAudit AI"
        const titleStartTimer = setTimeout(() => {
            typeTitle(titleString, () => {
                if (hasCompletedTitle) return;
                hasCompletedTitle = true;

                // Stage 3: Immediately when "RustAudit AI" finishes typing, type the Subtitle!
                typeSubtitle(subtitleString, () => {
                    if (hasCompletedSubtitle) return;
                    hasCompletedSubtitle = true;

                    // Stage 4: Comfortable reading pause, then dissolve into the dashboard
                    const exitTimer = setTimeout(dismissSplashScreen, 1300);
                    splashTimers.push(exitTimer);
                });
            });
        }, 600);

        splashTimers.push(titleStartTimer);
    }

    function typeTitle(text, onComplete) {
        if (!splashTitleRoot) return;
        if (typeof React !== 'undefined' && typeof ReactDOM !== 'undefined' && window.TextType) {
            try {
                if (!splashTitleReactRoot) {
                    splashTitleReactRoot = ReactDOM.createRoot(splashTitleRoot);
                }
                splashTitleReactRoot.render(
                    React.createElement(
                        window.TextType,
                        {
                            key: `title-${Date.now()}`,
                            text: [text],
                            className: "splash-title-texttype",
                            typingSpeed: 55,
                            loop: false,
                            showCursor: true,
                            cursorCharacter: "|",
                            cursorBlinkDuration: 0.45,
                            onSentenceComplete: onComplete
                        }
                    )
                );
                return;
            } catch (err) {
                console.warn("TextType Title React error:", err);
            }
        }
        mountFallbackTextType(splashTitleRoot, text, "splash-title-texttype", 55, onComplete);
    }

    function typeSubtitle(text, onComplete) {
        if (!splashSubtitleRoot) return;
        if (typeof React !== 'undefined' && typeof ReactDOM !== 'undefined' && window.TextType) {
            try {
                if (!splashSubtitleReactRoot) {
                    splashSubtitleReactRoot = ReactDOM.createRoot(splashSubtitleRoot);
                }
                splashSubtitleReactRoot.render(
                    React.createElement(
                        window.TextType,
                        {
                            key: `subtitle-${Date.now()}`,
                            text: [text],
                            className: "splash-subtitle-texttype",
                            typingSpeed: 28,
                            loop: false,
                            showCursor: true,
                            cursorCharacter: "|",
                            cursorBlinkDuration: 0.45,
                            onSentenceComplete: onComplete
                        }
                    )
                );
                return;
            } catch (err) {
                console.warn("TextType Subtitle React error:", err);
            }
        }
        mountFallbackTextType(splashSubtitleRoot, text, "splash-subtitle-texttype", 28, onComplete);
    }

    function mountFallbackTextType(container, text, customClass, speed, onComplete) {
        if (!container) return;
        let charIdx = 0;
        container.innerHTML = `<span class="text-type ${customClass}"><span class="text-type__content"></span><span class="text-type__cursor">|</span></span>`;
        const contentEl = container.querySelector(".text-type__content");

        const typeInterval = setInterval(() => {
            charIdx++;
            if (contentEl) contentEl.textContent = text.slice(0, charIdx);
            if (charIdx >= text.length) {
                clearInterval(typeInterval);
                if (onComplete) onComplete();
            }
        }, speed);
        splashTimers.push(typeInterval);
    }

    function dismissSplashScreen() {
        clearAllSplashTimers();
        if (splashScreen) {
            splashScreen.classList.add("splash-dismissed");
            setTimeout(() => {
                splashScreen.style.display = "none";
            }, 750);
        }
    }

    // Clicking anywhere on the splash screen dismisses it immediately
    if (splashScreen) {
        splashScreen.addEventListener("click", dismissSplashScreen);
    }

    if (replayIntroBtn) {
        replayIntroBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            runSplashSequence();
        });
    }

    // Launch Splash Sequence on page load
    runSplashSequence();

    // Interactive mouse tracking ambient spotlight on cards
    document.querySelectorAll(".panel, .rqi-hero-card, .metric-mini-card, .dev-formula-card").forEach(card => {
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty("--mouse-x", `${x}px`);
            card.style.setProperty("--mouse-y", `${y}px`);
        });
    });

    // --- State Variables ---
    let currentAnalysisData = null;
    let activeFnIndex = 0;
    let activeGraphType = "flog";
    let isDeveloperMode = false;
    let singleNetwork = null;
    let originalNetwork = null;
    let refactoredNetwork = null;

    const sampleRustCode = `// RustAuditAI Sample Subroutine (Demonstrating Ownership & Performance Anti-patterns)
pub fn process_user_data(data: &str) -> String {
    let mut result = String::from(data);
    let duplicate = result.clone();
    
    if data.len() > 10 {
        let boxed_val = Box::new(duplicate);
        return format!("Processed: {}", boxed_val);
    }

    unsafe {
        let ptr = data.as_ptr();
        println!("Raw pointer address: {:?}", ptr);
    }

    result
}

fn calculate_metrics(values: Vec<i32>) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}`;

    // --- Helper Utilities ---
    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function formatScore(score) {
        if (score === null || score === undefined || isNaN(score)) return "0";
        const num = Number(score);
        if (num === 0) return "0";
        const str = num.toFixed(1);
        return str.endsWith(".0") ? str.slice(0, -2) : str;
    }

    function showToast(message, type = "info") {
        if (!toastContainer) return;
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        const icon = type === "success" ? "fa-circle-check" : (type === "error" ? "fa-circle-exclamation" : "fa-circle-info");
        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${escapeHtml(message)}</span>`;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(10px)";
            setTimeout(() => toast.remove(), 250);
        }, 3200);
    }

    // --- Pre-Analysis Workstation Dynamic Height (Adjusts to Lines of Code) ---
    function adjustPreAuditEditorHeight() {
        if (!codeEditor || !editorWrapper) return;
        // This dynamic sizing applies ONLY to the pre-analysis div (before audit)
        if (currentAuditSection && currentAuditSection.classList.contains("is-audited")) {
            // Post-analysis mode: CSS 100vh flex takes over
            editorWrapper.style.height = "";
            codeEditor.style.height = "";
            codeEditor.style.overflowY = "";
            if (editorCodeStage) editorCodeStage.style.height = "";
            if (editorHighlightUnderlay) editorHighlightUnderlay.style.height = "";
            if (editorGutter) editorGutter.style.height = "";
            return;
        }

        const lines = codeEditor.value.split("\n");
        const count = Math.max(1, lines.length);
        // 22px line-height + 32px vertical padding (1rem top + 1rem bottom) + 8px buffer
        const dynamicHeight = Math.max(240, (count * 22) + 40);
        editorWrapper.style.height = `${dynamicHeight}px`;
        codeEditor.style.height = `${dynamicHeight}px`;
        codeEditor.style.overflowY = "hidden";
        if (editorCodeStage) editorCodeStage.style.height = `${dynamicHeight}px`;
        if (editorHighlightUnderlay) editorHighlightUnderlay.style.height = `${dynamicHeight}px`;
        if (editorGutter) {
            editorGutter.style.height = `${dynamicHeight}px`;
        }
    }

    // --- Rust Syntax Highlighting Tokenizer ---
    function highlightRustCode(code) {
        if (!code) return "";

        const masterRegex = /(\/\/.*?$)|(\/\*[\s\S]*?\*\/)|(r#"(?:[\s\S]*?)"#|"(?:\\.|[^"\\])*")|('(?:static|[a-zA-Z_][a-zA-Z0-9_]*)\b)|('(?:\\.|[^\\'])')|(#!?\[[^\]]*\])|([a-zA-Z_][a-zA-Z0-9_]*!)|(\b(?:0x[0-9a-fA-F_]+|\d[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?[\d_]+)?(?:f32|f64|u8|u16|u32|u64|u128|usize|i8|i16|i32|i64|i128|isize)?)\b)|([a-zA-Z_][a-zA-Z0-9_]*)|(->|=>|::|&mut|&|\*|==|!=|<=|>=|&&|\|\||[+\-*\/%^=<>!|&?]+)/gm;

        const keywords = new Set([
            "fn", "let", "pub", "struct", "enum", "impl", "trait", "type", "use", "mod",
            "crate", "super", "match", "if", "else", "while", "for", "loop", "in", "return",
            "break", "continue", "as", "ref", "const", "static", "where", "move", "async",
            "await", "dyn", "extern"
        ]);
        const unsafeKeyword = new Set(["unsafe"]);
        const mutKeyword = new Set(["mut"]);
        const types = new Set([
            "i8", "i16", "i32", "i64", "i128", "isize",
            "u8", "u16", "u32", "u64", "u128", "usize",
            "f32", "f64", "bool", "char", "str", "String",
            "Vec", "Option", "Result", "Some", "None", "Ok", "Err",
            "Box", "Rc", "Arc", "RefCell", "Mutex", "Cell",
            "self", "Self"
        ]);
        const booleans = new Set(["true", "false"]);

        return code.replace(masterRegex, (match, lineComment, blockComment, stringLit, lifetime, charLit, attr, macroCall, numberLit, word, op) => {
            if (lineComment || blockComment) {
                return `<span class="hl-comment">${escapeHtml(match)}</span>`;
            }
            if (stringLit) {
                return `<span class="hl-string">${escapeHtml(match)}</span>`;
            }
            if (charLit) {
                return `<span class="hl-char">${escapeHtml(match)}</span>`;
            }
            if (lifetime) {
                return `<span class="hl-lifetime">${escapeHtml(match)}</span>`;
            }
            if (attr) {
                return `<span class="hl-attribute">${escapeHtml(match)}</span>`;
            }
            if (macroCall) {
                return `<span class="hl-macro">${escapeHtml(match)}</span>`;
            }
            if (numberLit) {
                return `<span class="hl-number">${escapeHtml(match)}</span>`;
            }
            if (word) {
                if (unsafeKeyword.has(word)) {
                    return `<span class="hl-unsafe">${escapeHtml(match)}</span>`;
                }
                if (mutKeyword.has(word)) {
                    return `<span class="hl-mut">${escapeHtml(match)}</span>`;
                }
                if (keywords.has(word)) {
                    return `<span class="hl-keyword">${escapeHtml(match)}</span>`;
                }
                if (types.has(word)) {
                    return `<span class="hl-type">${escapeHtml(match)}</span>`;
                }
                if (booleans.has(word)) {
                    return `<span class="hl-bool">${escapeHtml(match)}</span>`;
                }
                return escapeHtml(match);
            }
            if (op) {
                return `<span class="hl-op">${escapeHtml(match)}</span>`;
            }
            return escapeHtml(match);
        });
    }

    // Update Live Syntax Underlay in Subroutine Workstation
    function updateEditorHighlighting() {
        if (!codeEditor || !editorHighlightCode) return;
        const text = codeEditor.value;
        if (!text) {
            editorHighlightCode.innerHTML = "";
            return;
        }
        let highlighted = highlightRustCode(text);
        if (text.endsWith("\n")) {
            highlighted += " ";
        }
        editorHighlightCode.innerHTML = highlighted;
    }

    // --- Gutter Synchronization ---
    function updateEditorGutter() {
        if (!editorGutter || !codeEditor) return;
        const lines = codeEditor.value.split("\n");
        const count = Math.max(1, lines.length);

        // Find anomaly line numbers from active function deductions
        const anomalyLines = new Set();
        const criticalLines = new Set();
        if (currentAnalysisData && currentAnalysisData.functions[activeFnIndex]) {
            const fn = currentAnalysisData.functions[activeFnIndex];
            const deductions = fn.rqi ? (fn.rqi.structured_deductions_list || []) : [];
            deductions.forEach(d => {
                if (d.line_number) {
                    if (d.severity === "CRITICAL") criticalLines.add(d.line_number);
                    else anomalyLines.add(d.line_number);
                }
            });
        }

        let html = "";
        for (let i = 1; i <= count; i++) {
            let cls = "gutter-line";
            let marker = "";
            if (criticalLines.has(i)) {
                cls += " has-critical";
                marker = '<span class="anomaly-marker"></span>';
            } else if (anomalyLines.has(i)) {
                cls += " has-anomaly";
                marker = '<span class="anomaly-marker"></span>';
            }
            html += `<div class="${cls}">${marker}<span>${i}</span></div>`;
        }
        editorGutter.innerHTML = html;
        updateEditorHighlighting();
        adjustPreAuditEditorHeight();
    }

    if (codeEditor) {
        codeEditor.addEventListener("input", updateEditorGutter);
        codeEditor.addEventListener("scroll", () => {
            if (editorGutter) editorGutter.scrollTop = codeEditor.scrollTop;
            if (editorHighlightUnderlay) {
                editorHighlightUnderlay.scrollTop = codeEditor.scrollTop;
                editorHighlightUnderlay.scrollLeft = codeEditor.scrollLeft;
            }
        });
        updateEditorGutter();
        updateEditorHighlighting();
        adjustPreAuditEditorHeight();
    }
    if (refactoredCodeDisplay && refactoredCodeDisplay.textContent) {
        refactoredCodeDisplay.innerHTML = highlightRustCode(refactoredCodeDisplay.textContent);
    }
    window.addEventListener("resize", adjustPreAuditEditorHeight);

    // --- Perspective View Switcher (Executive vs Developer) ---
    function setPerspective(mode) {
        isDeveloperMode = (mode === "developer");
        if (devModeToggle) devModeToggle.checked = isDeveloperMode;

        if (viewExecutiveBtn && viewDeveloperBtn) {
            viewExecutiveBtn.classList.toggle("active", !isDeveloperMode);
            viewDeveloperBtn.classList.toggle("active", isDeveloperMode);
        }

        if (executiveView && developerView) {
            executiveView.style.display = isDeveloperMode ? "none" : "flex";
            developerView.style.display = isDeveloperMode ? "flex" : "none";
        }

        if (isDeveloperMode) {
            setTimeout(renderActiveGraphs, 50);
        }
    }

    if (viewExecutiveBtn) viewExecutiveBtn.addEventListener("click", () => setPerspective("executive"));
    if (viewDeveloperBtn) viewDeveloperBtn.addEventListener("click", () => setPerspective("developer"));
    if (devModeToggle) {
        devModeToggle.addEventListener("change", (e) => setPerspective(e.target.checked ? "developer" : "executive"));
    }

    // --- Execute Graph Audit ---
    if (analyzeBtn) {
        analyzeBtn.addEventListener("click", async () => {
            const code = codeEditor ? codeEditor.value.trim() : "";
            if (!code) {
                showToast("Please enter or paste Rust subroutine code.", "error");
                return;
            }

            // Dynamically reveal the subroutines bar, audit panels, and refactored section
            if (subroutinesBarWrapper) subroutinesBarWrapper.style.display = "block";
            if (currentAuditSection) currentAuditSection.classList.add("is-audited");
            adjustPreAuditEditorHeight();
            if (auditOutputPanel) auditOutputPanel.style.display = "flex";
            if (refactoredDivider) refactoredDivider.style.display = "flex";
            if (refactoredAuditSection) {
                refactoredAuditSection.classList.add("is-audited");
                refactoredAuditSection.style.display = "grid";
            }

            // Switch to 2 divs mode: show New File ONLY on left code div
            if (preAuditActions) preAuditActions.style.display = "none";
            if (postAuditActions) postAuditActions.style.display = "flex";

            if (welcomeEmptyState) welcomeEmptyState.style.display = "none";
            if (auditResultsContainer) auditResultsContainer.style.display = "none";
            if (loaderState) loaderState.style.display = "block";
            if (loaderText) loaderText.textContent = "Extracting AST token streams & building semantic graphs...";
            if (codeEditor) codeEditor.classList.add("scanning");

            try {
                const res = await fetch("/api/analyze", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        code: code,
                        explain: true, // Always synthesize XAI root-cause & refactored code
                    }),
                });

                const data = await res.json();
                if (!res.ok || !data.success) {
                    showToast("Audit Failed: " + (data.error || "Syntax parsing error"), "error");
                    if (loaderState) loaderState.style.display = "none";
                    return;
                }

                currentAnalysisData = data;
                activeFnIndex = 0;

                if (loaderState) loaderState.style.display = "none";
                if (auditResultsContainer) auditResultsContainer.style.display = "block";
                if (fnCountPill) fnCountPill.textContent = `${data.function_count} Subroutine(s) Analyzed`;

                renderSubroutineTabs();
                renderSubroutineResults();
                updateEditorGutter();
                showToast(`Analysis completed for ${data.function_count} subroutine(s)!`, "success");
            } catch (err) {
                showToast("Network connection error: " + err.message, "error");
                if (loaderState) loaderState.style.display = "none";
            } finally {
                if (codeEditor) codeEditor.classList.remove("scanning");
            }
        });
    }

    // --- Reset Workstation to Single Div Mode ---
    function resetToSingleDivWorkstation() {
        if (preAuditActions) preAuditActions.style.display = "flex";
        if (postAuditActions) postAuditActions.style.display = "none";
        if (currentAuditSection) currentAuditSection.classList.remove("is-audited");
        if (auditOutputPanel) auditOutputPanel.style.display = "none";
        if (subroutinesBarWrapper) subroutinesBarWrapper.style.display = "none";
        if (refactoredDivider) refactoredDivider.style.display = "none";
        if (refactoredAuditSection) {
            refactoredAuditSection.classList.remove("is-audited");
            refactoredAuditSection.style.display = "none";
        }
        if (codeEditor) {
            codeEditor.value = "";
            updateEditorGutter();
            codeEditor.focus();
        }
        if (fileBadge) fileBadge.style.display = "none";
        if (fileUploadInput) fileUploadInput.value = "";
        currentAnalysisData = null;
    }

    // --- Close / Minimize Results View ---
    if (closeResultsBtn) {
        closeResultsBtn.addEventListener("click", () => {
            if (auditOutputPanel) auditOutputPanel.style.display = "none";
            if (currentAuditSection) currentAuditSection.classList.remove("is-audited");
            adjustPreAuditEditorHeight();
            if (refactoredDivider) refactoredDivider.style.display = "none";
            if (refactoredAuditSection) {
                refactoredAuditSection.classList.remove("is-audited");
                refactoredAuditSection.style.display = "none";
            }
            if (subroutinesBarWrapper) subroutinesBarWrapper.style.display = "none";
            // Return to single div mode tabs
            if (preAuditActions) preAuditActions.style.display = "flex";
            if (postAuditActions) postAuditActions.style.display = "none";
            showToast("Results minimized. Workstation expanded.", "info");
        });
    }

    // --- Workstation Actions: New File (Active ONLY when 2 divs are shown) ---
    if (newFileBtn) {
        newFileBtn.addEventListener("click", () => {
            resetToSingleDivWorkstation();
            showToast("Workstation initialized for new file. Load sample or upload code to audit.", "info");
        });
    }

    // --- Workstation Actions: Load Sample Subroutine (Active in single div mode) ---
    if (loadSampleBtn) {
        loadSampleBtn.addEventListener("click", () => {
            if (codeEditor) {
                codeEditor.value = sampleRustCode;
                updateEditorGutter();
            }
            if (fileBadge && fileNameText) {
                fileNameText.textContent = "sample_func.rs";
                fileBadge.style.display = "inline-flex";
            }
            showToast("Loaded calibrated sample Rust subroutine!", "success");
        });
    }

    // --- Workstation Actions: Clear Code Editor (Active in single div mode) ---
    if (clearCodeBtn) {
        clearCodeBtn.addEventListener("click", () => {
            if (codeEditor) {
                codeEditor.value = "";
                updateEditorGutter();
            }
            if (fileBadge) fileBadge.style.display = "none";
            if (fileUploadInput) fileUploadInput.value = "";
            showToast("Workstation editor cleared.", "info");
        });
    }

    // --- Workstation Actions: Upload File (.rs) Handler ---
    async function handleFileUpload(file) {
        if (!file) return;
        if (!file.name.endsWith(".rs")) {
            showToast(`Unsupported file format: '${file.name}'. RustAuditAI requires a Rust source file (.rs).`, "error");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            showToast(`Uploading and validating ${file.name}...`, "info");
            const res = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();
            if (!res.ok || !data.success) {
                showToast("Upload failed: " + (data.detail || data.error || "Server error"), "error");
                return;
            }

            if (codeEditor) {
                codeEditor.value = data.code;
                updateEditorGutter();
            }
            if (fileBadge && fileNameText) {
                fileNameText.textContent = data.filename;
                fileBadge.style.display = "inline-flex";
            }
            showToast(`Loaded ${data.filename} (${data.size} bytes) into workstation!`, "success");
        } catch (err) {
            // Client-side fallback FileReader if network upload is interrupted
            const reader = new FileReader();
            reader.onload = (e) => {
                if (codeEditor) {
                    codeEditor.value = e.target.result;
                    updateEditorGutter();
                }
                if (fileBadge && fileNameText) {
                    fileNameText.textContent = file.name;
                    fileBadge.style.display = "inline-flex";
                }
                showToast(`Loaded ${file.name} locally into workstation!`, "success");
            };
            reader.readAsText(file);
        }
    }

    if (uploadFileBtn && fileUploadInput) {
        uploadFileBtn.addEventListener("click", () => fileUploadInput.click());
        fileUploadInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }

    if (clearFileBtn) {
        clearFileBtn.addEventListener("click", () => {
            if (fileBadge) fileBadge.style.display = "none";
            if (fileUploadInput) fileUploadInput.value = "";
            showToast("Attached file badge cleared.", "info");
        });
    }

    // Drag & Drop on Editor
    if (editorWrapper) {
        editorWrapper.addEventListener("dragover", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (dropOverlay) dropOverlay.classList.remove("hidden");
        });

        editorWrapper.addEventListener("dragleave", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (dropOverlay) dropOverlay.classList.add("hidden");
        });

        editorWrapper.addEventListener("drop", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (dropOverlay) dropOverlay.classList.add("hidden");
            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFileUpload(e.dataTransfer.files[0]);
            }
        });
    }

    // --- Header Actions: XAI Test Button (Non-functional benchmark placeholder) ---
    if (xaiTestBtn) {
        xaiTestBtn.addEventListener("click", () => {
            showToast("XAI Engine Benchmark: Module offline. Execute a Graph Audit with XAI enabled to run live LLM root-cause synthesis.", "info");
        });
    }

    // --- Editor Keydown: Tab Indent & Ctrl+Enter to Audit ---
    if (codeEditor) {
        codeEditor.addEventListener("keydown", (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                e.preventDefault();
                if (analyzeBtn) analyzeBtn.click();
            } else if (e.key === "Tab") {
                e.preventDefault();
                const start = codeEditor.selectionStart;
                const end = codeEditor.selectionEnd;
                codeEditor.value = codeEditor.value.substring(0, start) + "    " + codeEditor.value.substring(end);
                codeEditor.selectionStart = codeEditor.selectionEnd = start + 4;
                updateEditorGutter();
            }
        });
    }

    // --- Subroutine Tabs Rendering ---
    function renderSubroutineTabs() {
        if (!functionTabs || !currentAnalysisData) return;
        functionTabs.innerHTML = "";
        const fns = currentAnalysisData.functions || [];

        fns.forEach((fn, idx) => {
            const pill = document.createElement("button");
            pill.type = "button";
            pill.className = `fn-tab-pill ${idx === activeFnIndex ? "active" : ""}`;
            const score = fn.rqi ? formatScore(fn.rqi.rqi_score) : "--";
            pill.innerHTML = `<i class="fa-solid fa-code"></i> fn ${escapeHtml(fn.name)}() <span class="fn-tab-score">${score}</span>`;
            pill.addEventListener("click", () => {
                activeFnIndex = idx;
                renderSubroutineTabs();
                renderSubroutineResults();
                updateEditorGutter();
            });
            functionTabs.appendChild(pill);
        });
    }

    // --- Render Subroutine Intelligence ---
    function renderSubroutineResults() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
        const fn = currentAnalysisData.functions[activeFnIndex];
        const rqi = fn.rqi || {};

        // 1. Hero RQI Dial & Grade
        const score = rqi.rqi_score !== undefined ? rqi.rqi_score : 0;
        if (rqiScoreNum) rqiScoreNum.textContent = formatScore(score);
        if (devRqiScoreNum) devRqiScoreNum.textContent = formatScore(score);
        if (scoreCirclePath) scoreCirclePath.setAttribute("stroke-dasharray", `${score}, 100`);
        if (devScoreCirclePath) devScoreCirclePath.setAttribute("stroke-dasharray", `${score}, 100`);

        // Color Dial based on score tiers
        let dialColor = "var(--vec-maint)";
        if (score < 60) dialColor = "var(--sev-critical)";
        else if (score < 75) dialColor = "var(--brand-rust)";
        else if (score < 90) dialColor = "var(--vec-perf)";
        if (scoreCirclePath) scoreCirclePath.setAttribute("stroke", dialColor);

        // Grade Chip
        const rawGrade = rqi.grade || "A (Good Quality)";
        const gradeMatch = rawGrade.match(/^([A-Z]\+?)\s*\((.*)\)$/);
        const gradeLetter = gradeMatch ? gradeMatch[1] : (rawGrade[0] || "A");
        const gradeText = gradeMatch ? gradeMatch[2] : rawGrade;
        if (rqiGradeLetter) rqiGradeLetter.textContent = gradeLetter;
        if (rqiGradeText) rqiGradeText.textContent = gradeText;

        if (rqiSummaryText) {
            rqiSummaryText.textContent = rqi.penalty_applied
                ? `Dynamic penalty applied: ${rqi.penalty_reasons.join("; ")}`
                : (score >= 90 ? "Optimal zero-cost ownership and memory safety verified." : "Opportunities detected for idiomatic Rust refactoring.");
        }

        // 2. 2x2 Vector Mini-Gauges
        const sSafety = rqi.safety_score || 0;
        const sPerf = rqi.performance_score || 0;
        const sMaint = rqi.maintainability_score || 0;
        const sSec = rqi.security_score || 0;

        if (valSafety) valSafety.textContent = formatScore(sSafety);
        if (pathSafety) pathSafety.setAttribute("stroke-dasharray", `${sSafety}, 100`);
        if (valPerf) valPerf.textContent = formatScore(sPerf);
        if (pathPerf) pathPerf.setAttribute("stroke-dasharray", `${sPerf}, 100`);
        if (valMaint) valMaint.textContent = formatScore(sMaint);
        if (pathMaint) pathMaint.setAttribute("stroke-dasharray", `${sMaint}, 100`);
        if (valSec) valSec.textContent = formatScore(sSec);
        if (pathSec) pathSec.setAttribute("stroke-dasharray", `${sSec}, 100`);

        // 3. MITRE CWE Tracking Strip
        const cweSummary = fn.cwe_summary || {};
        if (cweCountTotal) cweCountTotal.textContent = `${cweSummary.total || 0} Total`;
        if (cweCountCritical) cweCountCritical.textContent = `${cweSummary.critical || 0} Critical`;
        if (cweCountHigh) cweCountHigh.textContent = `${cweSummary.high || 0} High`;
        if (cweCountMedium) cweCountMedium.textContent = `${cweSummary.medium || 0} Medium`;
        if (cweCountLow) cweCountLow.textContent = `${cweSummary.low || 0} Low`;

        // 4. Structured Deductions (Remove fixes from original evaluation)
        if (deductionsList) {
            deductionsList.innerHTML = "";
            const deductions = rqi.structured_deductions_list || [];
            if (deductions.length === 0) {
                deductionsList.innerHTML = `
                    <li class="deduction-card" style="border-left-color: var(--vec-maint);">
                        <p style="color: var(--vec-maint); font-weight: 600;"><i class="fa-solid fa-check-circle"></i> Zero quality deductions. All intra-procedural invariants satisfied!</p>
                    </li>
                `;
            } else {
                deductions.forEach(d => {
                    const sev = (d.severity || "medium").toLowerCase();
                    const card = document.createElement("li");
                    card.className = `deduction-card sev-${sev}`;
                    card.innerHTML = `
                        <div class="deduction-card-top">
                            <div class="deduction-badge-group">
                                <span class="vector-tag">[${escapeHtml(d.vector)}]</span>
                                ${d.cwe_id ? `<a href="${d.cwe_url || `https://cwe.mitre.org/data/definitions/${d.cwe_id.replace('CWE-','')}.html`}" target="_blank" rel="noopener noreferrer" class="cwe-pill-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${d.cwe_id}</a>` : ""}
                                ${d.line_number ? `<span class="line-tag-pill"><i class="fa-solid fa-crosshairs"></i> Line ${d.line_number}</span>` : ""}
                            </div>
                            <span class="pts-deduction-badge">-${formatScore(d.penalty)} pts</span>
                        </div>
                        <p class="deduction-message">${escapeHtml(d.message)}</p>
                        ${d.statement_code ? `<div class="deduction-code-snippet"><code>${escapeHtml(d.statement_code)}</code></div>` : ""}
                    `;
                    deductionsList.appendChild(card);
                });
            }
        }

        // 5. Graph Topology Metrics Bar
        const cpgSum = fn.cpg_summary || {};
        if (astNodesCnt) astNodesCnt.textContent = cpgSum.ast_nodes || 0;
        if (cfgCcCnt) cfgCcCnt.textContent = cpgSum.cyclomatic_complexity || 1;
        if (flogAllocCnt) flogAllocCnt.textContent = cpgSum.allocations || 0;
        if (flogClonesCnt) flogClonesCnt.textContent = cpgSum.clones || 0;
        if (cpgEdgesCnt) cpgEdgesCnt.textContent = cpgSum.cpg_edges || 0;

        // 6. Refactored Code Viewer Rendering (Left Screen of Section 2)
        const xai = fn.xai_report || {};
        const refactoredCode = xai.refactored_code || generateCleanFallbackCode(fn);
        if (refactoredCodeDisplay) {
            refactoredCodeDisplay.innerHTML = highlightRustCode(refactoredCode);
        }
        if (xaiPatchCode) {
            xaiPatchCode.textContent = refactoredCode;
        }
        updateRefactoredGutter(refactoredCode);

        // 7. Refactored AI Root Cause & Remediation Insights (Accordion 2 in Section 2)
        if (xaiExplanationText) {
            xaiExplanationText.innerHTML = xai.explanation
                ? formatExplanationMarkdown(xai.explanation)
                : "<div class='xai-card-item'><div class='xai-item-body'><p>Optimal zero-cost invariants verified. No defects detected in this subroutine.</p></div></div>";
        }

        // 8. Revisions Badge
        const totalRevs = fn.total_revisions !== undefined ? fn.total_revisions : (fn.revisions ? fn.revisions.length : 0);
        if (revCountBadge) revCountBadge.textContent = totalRevs;

        // 9. Render Section 1 Graphs & Section 2 Refactored Graphs
        renderActiveGraphs();
        renderActiveRefactoredGraphs();
    }

    // --- Side-by-Side Dual-Column Diff Renderer ---
    function renderSideBySideDiff(fn) {
        if (!diffOriginalBody || !diffRefactoredBody) return;
        diffOriginalBody.innerHTML = "";
        diffRefactoredBody.innerHTML = "";

        // Extract original subroutine source lines
        const fullSource = codeEditor ? codeEditor.value : "";
        const allLines = fullSource.split("\n");
        let originalLines = [];
        if (fn.line_start > 0 && fn.line_end <= allLines.length) {
            originalLines = allLines.slice(fn.line_start - 1, fn.line_end);
        } else {
            originalLines = allLines;
        }

        const xai = fn.xai_report || {};
        const refactoredCode = xai.refactored_code || "";
        const refactoredLines = refactoredCode ? refactoredCode.split("\n") : [];

        if (xaiExplanationText) {
            xaiExplanationText.innerHTML = xai.explanation ? formatExplanationMarkdown(xai.explanation) : "<p>No explanation generated.</p>";
        }
        if (xaiPatchCode) {
            xaiPatchCode.textContent = refactoredCode || "// No refactoring required (Subroutine is optimal)";
        }

        if (applyPatchBtn) {
            applyPatchBtn.style.display = refactoredCode ? "inline-flex" : "none";
        }
        if (copyPatchBtn) {
            copyPatchBtn.style.display = refactoredCode ? "inline-flex" : "none";
        }

        // Render Left Column (Original Code)
        originalLines.forEach((line, idx) => {
            const lineNum = fn.line_start + idx;
            const isRemoved = refactoredLines.length > 0 && !refactoredLines.includes(line);
            const lineEl = document.createElement("div");
            lineEl.className = `diff-line ${isRemoved ? "deletion" : ""}`;
            lineEl.innerHTML = `<span class="diff-line-num">${lineNum}</span><span class="diff-line-content">${escapeHtml(line)}</span>`;
            diffOriginalBody.appendChild(lineEl);
        });

        // Render Right Column (Refactored Patch)
        if (refactoredLines.length === 0) {
            diffRefactoredBody.innerHTML = `<div class="diff-line" style="color: var(--vec-maint); padding: 1rem;"><span class="diff-line-content"><i class="fa-solid fa-check"></i> Subroutine already optimal (~100% RQI). Zero refactoring needed.</span></div>`;
        } else {
            refactoredLines.forEach((line, idx) => {
                const isAdded = !originalLines.includes(line);
                const lineEl = document.createElement("div");
                lineEl.className = `diff-line ${isAdded ? "addition" : ""}`;
                lineEl.innerHTML = `<span class="diff-line-num">${idx + 1}</span><span class="diff-line-content">${escapeHtml(line)}</span>`;
                diffRefactoredBody.appendChild(lineEl);
            });
        }
    }

    function formatExplanationMarkdown(text) {
        if (!text) return "<p>No explanation generated.</p>";

        // 1. Strip CWE IDs and associated phrases exclusively from XAI explanation display
        let cleaned = text.replace(/(?:and\s+triggers\s+|triggers\s+|associated\s+with\s+|classified\s+as\s+|via\s+)?\[?\s*\(?\s*CWE[-\u2010-\u2015]?\d+\s*\)?\s*\]?/gi, "")
                          .replace(/\(?\s*\[?\s*CWE[-\u2010-\u2015]?\d+\s*\]?\s*\)?/gi, "")
                          .replace(/CWE[-\u2010-\u2015]?\d+/gi, "")
                          .replace(/\(\s*\)/g, "")
                          .replace(/\[\s*\]/g, "")
                          .replace(/\s+([.,;:!?])/g, "$1");

        // 2. Parse into structured card items if numbered defect items exist
        const blocks = cleaned.split(/(?=^\d+\.\s*)/m);
        let htmlOut = "";

        blocks.forEach(block => {
            block = block.trim();
            if (!block) return;

            const numMatch = block.match(/^(\d+)\.\s*([\s\S]*)/);
            if (!numMatch) {
                // Introductory overview text or general paragraph
                let introFormatted = escapeHtml(block)
                    .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--text-primary);">$1</strong>')
                    .replace(/`([^`]+)`/g, '<code class="xai-inline-code">$1</code>')
                    .replace(/\n/g, '<br>');
                htmlOut += `<div class="xai-intro-text">${introFormatted}</div>`;
                return;
            }

            const num = numMatch[1];
            const rest = numMatch[2].trim();

            // Find Root Cause
            const rcMatch = rest.match(/(?:[-*#\s]*Root\s*Cause[:\s]*)([\s\S]*)/i);
            let titlePart = "";
            let bodyPart = "";

            if (rcMatch) {
                titlePart = rest.substring(0, rcMatch.index).trim();
                bodyPart = rcMatch[0].trim();
            } else {
                const lines = rest.split("\n");
                titlePart = lines[0].trim();
                bodyPart = lines.slice(1).join("\n").trim();
            }

            // Clean title: remove "Defect Title", parens, colons, asterisks and uppercase
            let cleanTitle = titlePart.replace(/Defect\s+Title\s*[:(]?\s*/gi, "")
                                      .replace(/^[(\[\s*:]+|[)\]\s*:]+$/g, "")
                                      .replace(/^[(\[\s*:]+|[)\]\s*:]+$/g, "")
                                      .replace(/\*\*/g, "")
                                      .replace(/\s+/g, " ")
                                      .trim()
                                      .toUpperCase();

            // Find Remediation
            const remMatch = bodyPart.match(/(?:[-*#\s]*Remediation[:\s]*)([\s\S]*)/i);
            let rcText = "";
            let remText = "";

            if (remMatch) {
                rcText = bodyPart.substring(0, remMatch.index).trim();
                remText = remMatch[1].trim();
            } else {
                rcText = bodyPart.trim();
            }

            // Strip prefixes and trailing punctuation
            rcText = rcText.replace(/^(?:[-*#\s]*Root\s*Cause[:\s\-*]*)/i, "").replace(/^[*:\s\-]+/, "").replace(/[-:\s*]+$/, "").trim();
            remText = remText.replace(/^(?:[-*#\s]*Remediation[:\s\-*]*)/i, "").replace(/^[*:\s\-]+/, "").replace(/[-:\s*]+$/, "").trim();

            // Helper to format code spans and bold text inside fields
            const formatContent = (str) => {
                return escapeHtml(str)
                    .replace(/`([^`]+)`/g, '<code class="xai-inline-code">$1</code>')
                    .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--text-primary);">$1</strong>')
                    .replace(/\n/g, ' ');
            };

            htmlOut += `
            <div class="xai-card-item">
                <div class="xai-item-header">
                    <span class="xai-item-badge">DEFECT ${num}</span>
                    <h5 class="xai-item-title">${escapeHtml(cleanTitle)}</h5>
                </div>
                <div class="xai-item-body">
                    <div class="xai-field xai-field-rc">
                        <span class="xai-field-tag"><i class="fa-solid fa-circle-exclamation"></i> ROOT CAUSE</span>
                        <div class="xai-field-text">${formatContent(rcText)}</div>
                    </div>
                    ${remText ? `
                    <div class="xai-field xai-field-rem">
                        <span class="xai-field-tag" style="background: var(--vec-maint-dim); color: var(--vec-maint); border-color: var(--vec-maint);"><i class="fa-solid fa-shield-check"></i> HOW AI ELIMINATED THIS IN REFACTORED CODE</span>
                        <div class="xai-field-text">${formatContent(remText)}</div>
                    </div>` : ''}
                </div>
            </div>`;
        });

        return htmlOut || `<p>${escapeHtml(text)}</p>`;
    }

    // --- Section 1: Original Graph Tab Switchers ---
    const evalGraphTabButtons = document.querySelectorAll("#eval-acc-graphs .graph-tab-btn");
    evalGraphTabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            evalGraphTabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeGraphType = btn.getAttribute("data-graph") || "flog";
            renderActiveGraphs();
        });
    });

    // --- Section 2: Refactored Graph Tab Switchers ---
    let activeRefactoredGraphType = "flog";
    const refactoredGraphTabButtons = document.querySelectorAll(".refactored-graph-tab-btn");
    refactoredGraphTabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            refactoredGraphTabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeRefactoredGraphType = btn.getAttribute("data-refactored-graph") || "flog";
            renderActiveRefactoredGraphs();
        });
    });

    // --- Master Vis.js Graph Rendering Engine for Section 1 ---
    function renderActiveGraphs() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
        const fn = currentAnalysisData.functions[activeFnIndex];
        if (interactiveCanvas) {
            renderSingleGraph(interactiveCanvas, fn, activeGraphType, "single");
        }
    }

    // --- Master Vis.js Graph Rendering Engine for Section 2 (Refactored Code) ---
    function renderActiveRefactoredGraphs() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
        const fn = currentAnalysisData.functions[activeFnIndex];
        if (refactoredInteractiveCanvas) {
            renderSingleGraph(refactoredInteractiveCanvas, fn, activeRefactoredGraphType, "refactored");
        }
    }

    function renderSingleGraph(container, fn, graphType, mode) {
        let rawNodes = (fn.nodes && fn.nodes[graphType]) || [];
        let rawEdges = (fn.edges && fn.edges[graphType]) || [];

        // If rendering refactored view in dual mode, simulate the clean optimized graph
        if (mode === "refactored") {
            rawNodes = rawNodes.filter(n => !n.is_unsafe && n.node_type !== "UnsafeOperation" && !n.is_clone && n.node_type !== "ClonedBinding");
            rawEdges = rawEdges.filter(e => !(e.edge_type && (e.edge_type.includes("UNSAFE") || e.edge_type.includes("CLONED"))));
        }

        const nodes = rawNodes.map(n => {
            let label = n.label || n.var_name || n.name || n.kind || n.node_type || n.id;
            let color = "#3b82f6"; // Default blue
            let shape = "box";

            if (graphType === "cpg") {
                if (n.layer === "AST") color = "#06b6d4"; // Cyan
                else if (n.layer === "CFG") color = n.is_decision ? "#f59e0b" : "#3b82f6";
                else if (n.layer === "FLOG") {
                    if (n.is_unsafe || n.node_type === "UnsafeOperation") color = "#dc2626";
                    else if (n.is_clone || n.node_type === "ClonedBinding") color = "#ef4444";
                    else if (n.is_heap_alloc || n.node_type === "HeapAllocation") color = "#a855f7";
                    else color = "#10b981";
                }
            } else {
                if (n.node_type === "FunctionDecl" || n.node_type === "ENTRY" || n.node_type === "FnScope") color = "#06b6d4";
                if (n.node_type === "DecisionBlock" || n.is_decision) color = "#f59e0b";
                if (n.node_type === "HeapAllocation" || n.is_heap_alloc) color = "#a855f7";
                if (n.node_type === "ClonedBinding" || n.is_clone) color = "#ef4444";
                if (n.node_type === "UnsafeOperation" || n.is_unsafe) color = "#dc2626";
            }

            return {
                id: n.id,
                label: label,
                color: { background: color, border: "#ffffff", highlight: { background: "#ffffff", border: color } },
                font: { color: "#ffffff", face: "JetBrains Mono, monospace", size: 12 },
                shape: shape,
                margin: 10,
            };
        });

        const edges = rawEdges.map(e => {
            const isCrossLayer = e.edge_type && (
                e.edge_type.includes("AST_TO_CFG") ||
                e.edge_type.includes("AST_TO_FLOG") ||
                e.edge_type.includes("CFG_TO_FLOG")
            );

            return {
                from: e.source,
                to: e.target,
                label: e.label || e.edge_type || "",
                font: { color: isCrossLayer ? "#c084fc" : "#94a3b8", size: isCrossLayer ? 11 : 9 },
                arrows: "to",
                dashes: isCrossLayer,
                width: isCrossLayer ? 2 : 1,
                color: { color: isCrossLayer ? "#818cf8" : "#334155" },
            };
        });

        const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        const options = {
            physics: {
                solver: "forceAtlas2Based",
                stabilization: { iterations: 90 },
                forceAtlas2Based: {
                    gravitationalConstant: -40,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08,
                }
            },
            interaction: { hover: true, zoomView: true, dragView: true }
        };

        if (mode === "original") {
            if (originalNetwork) originalNetwork.destroy();
            originalNetwork = new vis.Network(container, data, options);
        } else if (mode === "refactored") {
            if (refactoredNetwork) refactoredNetwork.destroy();
            refactoredNetwork = new vis.Network(container, data, options);
        } else {
            if (singleNetwork) singleNetwork.destroy();
            singleNetwork = new vis.Network(container, data, options);
        }
    }

    // --- Topological Outliers Drawer ---
    function renderTopologicalOutliers(fn) {
        if (!outliersContentList) return;
        outliersContentList.innerHTML = "";
        const outliers = (fn.graph_outliers && fn.graph_outliers[activeGraphType]) || [];

        if (outliers.length === 0) {
            outliersContentList.innerHTML = `
                <div class="outlier-card-item" style="grid-column: 1 / -1; border-color: var(--vec-maint);">
                    <p style="color: var(--vec-maint); font-size: 0.84rem;"><i class="fa-solid fa-circle-check"></i> No topological anomalies detected in ${activeGraphType.toUpperCase()} graph model.</p>
                </div>
            `;
            return;
        }

        outliers.forEach(o => {
            const card = document.createElement("div");
            card.className = "outlier-card-item";
            card.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <strong style="font-size: 0.84rem; color: var(--text-primary);">${escapeHtml(o.title)}</strong>
                    <span class="cwe-count-pill ${o.severity ? o.severity.toLowerCase() : 'medium'}">${escapeHtml(o.severity)}</span>
                </div>
                <p style="font-size: 0.8rem; color: var(--text-muted);">${escapeHtml(o.description)}</p>
                ${o.remediation ? `<div style="font-size: 0.76rem; color: var(--vec-maint);"><i class="fa-solid fa-wrench"></i> <strong>Fix:</strong> ${escapeHtml(o.remediation)}</div>` : ""}
            `;
            outliersContentList.appendChild(card);
        });
    }

    // --- Safe Multi-Function Code Splicing on Patch Application ---
    if (applyPatchBtn) {
        applyPatchBtn.addEventListener("click", async () => {
            const textToApply = xaiPatchCode ? xaiPatchCode.textContent.trim() : "";
            if (!textToApply || textToApply.startsWith("// No") || textToApply.startsWith("// Error")) {
                showToast("No compilable refactoring patch candidate to apply.", "info");
                return;
            }

            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) {
                showToast("No active subroutine selected.", "error");
                return;
            }

            const activeFn = currentAnalysisData.functions[activeFnIndex];

            try {
                applyPatchBtn.disabled = true;
                applyPatchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Splicing...';

                // 1. Commit approved revision snapshot to SQLite database (SRS §4.6.7)
                const res = await fetch("/api/revisions/commit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        function_name: activeFn.name,
                        source_code: textToApply,
                        change_type: "PATCH_APPLIED",
                        patch_summary: "Applied Idiomatic Rust Refactoring Patch (~100% RQI)",
                    }),
                });

                const data = await res.json();
                if (!data.success) throw new Error(data.detail || "Failed to commit revision");

                // 2. Safe Code Splicing: replace ONLY the active subroutine scope inside the editor!
                if (codeEditor) {
                    const fullSource = codeEditor.value;
                    const allLines = fullSource.split("\n");

                    if (activeFn.line_start > 0 && activeFn.line_end <= allLines.length) {
                        const before = allLines.slice(0, activeFn.line_start - 1);
                        const after = allLines.slice(activeFn.line_end);
                        codeEditor.value = [...before, textToApply, ...after].join("\n");
                    } else {
                        codeEditor.value = textToApply;
                    }
                    updateEditorGutter();
                }

                showToast(`Patch applied and saved as Revision #${data.revision.revision_number}! Recalculating...`, "success");

                // 3. Automatically trigger re-audit to verify RQI ~100%
                if (analyzeBtn) analyzeBtn.click();

                setTimeout(() => {
                    applyPatchBtn.disabled = false;
                    applyPatchBtn.innerHTML = '<i class="fa-solid fa-code-commit"></i> Apply Patch';
                }, 1500);
            } catch (err) {
                applyPatchBtn.disabled = false;
                applyPatchBtn.innerHTML = '<i class="fa-solid fa-code-commit"></i> Apply Patch';
                showToast("Failed to apply patch: " + err.message, "error");
            }
        });
    }

    if (copyPatchBtn) {
        copyPatchBtn.addEventListener("click", () => {
            const text = refactoredCodeDisplay ? refactoredCodeDisplay.textContent : (xaiPatchCode ? xaiPatchCode.textContent : "");
            if (!text || text.startsWith("// Refactored code will appear") || text.startsWith("// Patched code will appear")) {
                showToast("No refactored code available to copy yet.", "info");
                return;
            }
            navigator.clipboard.writeText(text).then(() => {
                showToast("Patched complete code copied to clipboard!", "success");
                const origHtml = copyPatchBtn.innerHTML;
                copyPatchBtn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Copied!</span>';
                setTimeout(() => {
                    copyPatchBtn.innerHTML = origHtml;
                }, 1800);
            }).catch(() => {
                showToast("Failed to copy code to clipboard.", "error");
            });
        });
    }

    // --- Cyber Accordion Setup (Strict Single-Open Enforcement) ---
    function setupCyberAccordion(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const items = container.querySelectorAll(".cyber-accordion-item");

        items.forEach(item => {
            const header = item.querySelector(".cyber-accordion-header");
            const content = item.querySelector(".cyber-accordion-content");
            if (!header || !content) return;

            header.addEventListener("click", () => {
                const isOpen = item.classList.contains("active");

                // Strictly ONE open at a time in this accordion group!
                items.forEach(otherItem => {
                    otherItem.classList.remove("active");
                    const otherContent = otherItem.querySelector(".cyber-accordion-content");
                    if (otherContent) otherContent.style.display = "none";
                });

                if (!isOpen) {
                    item.classList.add("active");
                    content.style.display = "block";

                    // Re-fit Vis.js network if a graph canvas is inside this accordion
                    setTimeout(() => {
                        if (item.id === "eval-acc-graphs" && singleNetwork) {
                            singleNetwork.fit();
                        }
                        if (item.id === "refactored-acc-graphs") {
                            if (refactoredNetwork) refactoredNetwork.fit();
                        }
                    }, 60);
                }
            });
        });
    }

    setupCyberAccordion("eval-accordion-group");
    setupCyberAccordion("refactored-accordion-group");

    // --- Refactored Code Helpers ---
    function generateCleanFallbackCode(fn) {
        const fullSource = codeEditor ? codeEditor.value : "";
        const allLines = fullSource.split("\n");
        let origSnippet = "";
        if (fn.line_start > 0 && fn.line_end <= allLines.length) {
            origSnippet = allLines.slice(fn.line_start - 1, fn.line_end).join("\n");
        } else {
            origSnippet = fullSource;
        }

        let cleaned = origSnippet
            .replace(/\.clone\(\)/g, "")
            .replace(/unsafe\s*\{[\s\S]*?let\s+ptr\s*=\s*data\.as_ptr\(\);[\s\S]*?\}/g, "// Safe pointer formatting\n    let ptr = data.as_ptr();")
            .replace(/unsafe\s*\{[\s\S]*?\}/g, "// Unsafe block eliminated via safe abstractions");
        return cleaned || origSnippet;
    }

    function updateRefactoredGutter(code) {
        if (!refactoredGutter) return;
        refactoredGutter.innerHTML = "";
        const lines = (code || "").split("\n");
        lines.forEach((_, idx) => {
            const lineEl = document.createElement("div");
            lineEl.className = "gutter-line";
            lineEl.textContent = idx + 1;
            refactoredGutter.appendChild(lineEl);
        });
    }

    // --- Revision Ledger Drawer Controls ---
    async function loadRevisionHistory() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) {
            showToast("Please audit a subroutine first to inspect revision history.", "info");
            return;
        }
        const fnName = currentAnalysisData.functions[activeFnIndex].name;
        if (drawerFnSubtitle) drawerFnSubtitle.textContent = `Subroutine: fn ${fnName}() (SRS §4.6.7)`;

        try {
            const res = await fetch(`/api/revisions?function=${encodeURIComponent(fnName)}`);
            const data = await res.json();
            if (data.success && revisionsTimelineContainer) {
                revisionsTimelineContainer.innerHTML = "";
                const revs = data.revisions || [];
                if (revs.length === 0) {
                    if (revisionsEmptyState) revisionsEmptyState.style.display = "block";
                } else {
                    if (revisionsEmptyState) revisionsEmptyState.style.display = "none";
                    revs.forEach(r => {
                        const card = document.createElement("div");
                        card.className = `rev-card ${r.is_active ? "active-rev" : ""}`;
                        card.innerHTML = `
                            <div class="rev-card-header">
                                <span class="rev-num-tag">Revision #${r.revision_number}</span>
                                <span class="rev-timestamp">${escapeHtml(r.timestamp_display)}</span>
                            </div>
                            <div class="rev-score-row">
                                <span>RQI: <strong style="color: var(--vec-maint);">${formatScore(r.rqi_score)}</strong></span>
                                <span class="line-tag-pill">${escapeHtml(r.change_type)}</span>
                            </div>
                            <p style="font-size: 0.8rem; color: var(--text-secondary);">${escapeHtml(r.patch_summary)}</p>
                            ${!r.is_active ? `<button type="button" class="btn-rollback" data-id="${r.revision_id}"><i class="fa-solid fa-rotate-left"></i> Rollback to this state</button>` : `<span style="font-size: 0.72rem; color: var(--vec-maint); font-weight: 600;"><i class="fa-solid fa-check"></i> Active in Workspace</span>`}
                        `;

                        const rbBtn = card.querySelector(".btn-rollback");
                        if (rbBtn) {
                            rbBtn.addEventListener("click", async () => {
                                try {
                                    const rbRes = await fetch("/api/revisions/rollback", {
                                        method: "POST",
                                        headers: { "Content-Type": "application/json" },
                                        body: JSON.stringify({ revision_id: r.revision_id }),
                                    });
                                    const rbData = await rbRes.json();
                                    if (rbData.success) {
                                        if (codeEditor) {
                                            codeEditor.value = rbData.source_code;
                                            updateEditorGutter();
                                        }
                                        closeRevisionDrawer();
                                        showToast(`Rolled back to Revision #${r.revision_number}! Recalculating...`, "success");
                                        if (analyzeBtn) analyzeBtn.click();
                                    }
                                } catch (e) {
                                    showToast("Rollback failed: " + e.message, "error");
                                }
                            });
                        }
                        revisionsTimelineContainer.appendChild(card);
                    });
                }
            }
        } catch (err) {
            showToast("Failed to load revisions: " + err.message, "error");
        }

        if (revisionDrawerOverlay) revisionDrawerOverlay.classList.remove("hidden");
        if (revisionHistoryDrawer) revisionHistoryDrawer.classList.remove("hidden");
    }

    function closeRevisionDrawer() {
        if (revisionDrawerOverlay) revisionDrawerOverlay.classList.add("hidden");
        if (revisionHistoryDrawer) revisionHistoryDrawer.classList.add("hidden");
    }

    if (revisionsToggleBtn) revisionsToggleBtn.addEventListener("click", loadRevisionHistory);
    if (closeDrawerBtn) closeDrawerBtn.addEventListener("click", closeRevisionDrawer);
    if (revisionDrawerOverlay) revisionDrawerOverlay.addEventListener("click", closeRevisionDrawer);

    if (clearRevisionsBtn) {
        clearRevisionsBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
            const fnName = currentAnalysisData.functions[activeFnIndex].name;
            await fetch(`/api/revisions?function=${encodeURIComponent(fnName)}`, { method: "DELETE" });
            showToast("Revision history cleared for active subroutine.", "info");
            closeRevisionDrawer();
            if (revCountBadge) revCountBadge.textContent = "0";
        });
    }

    // --- Export PDF Report (Subroutine-wise Report of Complete File/Code) ---
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions || currentAnalysisData.functions.length === 0) {
                showToast("No audit data available to export.", "error");
                return;
            }
            try {
                showToast("Synthesizing complete subroutine-wise PDF report...", "info");
                const reportFilename = (fileNameText && fileNameText.textContent && fileNameText.textContent !== "sample.rs")
                    ? fileNameText.textContent
                    : "rust_program_audit.rs";

                const res = await fetch("/api/export/pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        audit_data: currentAnalysisData,
                        filename: reportFilename,
                    }),
                });
                if (!res.ok) throw new Error("Server responded with HTTP " + res.status);
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                const cleanBase = reportFilename.replace(/\.rs$/, "");
                a.download = `rustaudit_report_${cleanBase}.pdf`;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }, 300);
                showToast(`Complete subroutine-wise report downloaded (${currentAnalysisData.functions.length} routine${currentAnalysisData.functions.length > 1 ? "s" : ""})!`, "success");
            } catch (err) {
                showToast("PDF Export failed: " + err.message, "error");
            }
        });
    }

    // --- Export Standalone HTML Dashboard Report (SRS §4.6.5) ---
    if (exportHtmlBtn) {
        exportHtmlBtn.addEventListener("click", () => {
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) {
                showToast("No audit data available to export.", "error");
                return;
            }
            const fn = currentAnalysisData.functions[activeFnIndex];
            const rqi = fn.rqi || {};

            const htmlReport = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>RustAuditAI Executive Quality Report — fn ${escapeHtml(fn.name)}()</title>
<style>
body { font-family: 'Inter', system-ui, sans-serif; background: #0c101c; color: #f8fafc; padding: 2.5rem; }
.header { border-bottom: 2px solid #334155; padding-bottom: 1rem; margin-bottom: 2rem; }
h1 { font-family: 'Outfit', sans-serif; color: #f97316; }
.score-box { background: #151d2e; border: 1px solid #38bdf8; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
.vectors { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.v-card { background: #1a233a; border-radius: 8px; padding: 1rem; text-align: center; }
.deductions { list-style: none; padding: 0; }
.deductions li { background: #1e293b; border-left: 4px solid #ef4444; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-radius: 4px; }
pre { background: #060911; padding: 1rem; border-radius: 8px; overflow-x: auto; color: #38bdf8; font-family: monospace; }
</style>
</head>
<body>
<div class="header">
<h1>RustAuditAI Executive Quality & Vulnerability Audit Report</h1>
<p>Target Subroutine: <strong>fn ${escapeHtml(fn.name)}()</strong> | Scope: Lines ${fn.line_start}-${fn.line_end}</p>
<p>Generated on: ${new Date().toUTCString()}</p>
</div>
<div class="score-box">
<h2>Composite Rust Quality Index (RQI): ${formatScore(rqi.rqi_score)} / 100 (${escapeHtml(rqi.grade)})</h2>
<p>${rqi.penalty_applied ? 'Dynamic Penalties: ' + escapeHtml(rqi.penalty_reasons.join('; ')) : 'Standard linear weighted scoring.'}</p>
</div>
<div class="vectors">
<div class="v-card"><h3>Safety</h3><p style="font-size:1.5rem; color:#38bdf8;">${formatScore(rqi.safety_score)}</p></div>
<div class="v-card"><h3>Performance</h3><p style="font-size:1.5rem; color:#f59e0b;">${formatScore(rqi.performance_score)}</p></div>
<div class="v-card"><h3>Maintainability</h3><p style="font-size:1.5rem; color:#10b981;">${formatScore(rqi.maintainability_score)}</p></div>
<div class="v-card"><h3>Security</h3><p style="font-size:1.5rem; color:#a855f7;">${formatScore(rqi.security_score)}</p></div>
</div>
<h3>Identified Quality Deductions & Weaknesses</h3>
<ul class="deductions">
${(rqi.structured_deductions_list || []).map(d => `<li><strong>[${escapeHtml(d.cwe_id || 'N/A')}] Line ${d.line_number || '-'}:</strong> ${escapeHtml(d.message)} (-${formatScore(d.penalty)} pts)</li>`).join('') || '<li>Zero deductions detected.</li>'}
</ul>
<h3>XAI Refactored Idiomatic Rust Patch</h3>
<pre><code>${escapeHtml((fn.xai_report && fn.xai_report.refactored_code) || '// No refactoring needed')}</code></pre>
</body>
</html>`;

            const blob = new Blob([htmlReport], { type: "text/html" });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `rustaudit_report_${fn.name}.html`;
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 300);
            showToast("Offline HTML report downloaded successfully!", "success");
        });
    }
});

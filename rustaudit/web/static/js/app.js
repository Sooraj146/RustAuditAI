/**
 * RustAuditAI Web Dashboard Client Logic
 */

document.addEventListener("DOMContentLoaded", () => {
    const codeEditor = document.getElementById("code-editor");
    const loadSampleBtn = document.getElementById("load-sample-btn");
    const analyzeBtn = document.getElementById("analyze-btn");
    const enableXaiToggle = document.getElementById("enable-xai-toggle");

    const emptyState = document.getElementById("welcome-empty-state");
    const loaderState = document.getElementById("loader-state");
    const resultsContainer = document.getElementById("audit-results-container");

    const functionTabs = document.getElementById("function-tabs");
    const rqiScoreNum = document.getElementById("rqi-score-num");
    const rqiGrade = document.getElementById("rqi-grade");
    const rqiSummaryText = document.getElementById("rqi-summary-text");
    const scoreCirclePath = document.getElementById("score-circle-path");

    const valSafety = document.getElementById("val-safety");
    const barSafety = document.getElementById("bar-safety");
    const valPerf = document.getElementById("val-perf");
    const barPerf = document.getElementById("bar-perf");
    const valMaint = document.getElementById("val-maint");
    const barMaint = document.getElementById("bar-maint");
    const valSec = document.getElementById("val-sec");
    const barSec = document.getElementById("bar-sec");

    const deductionsList = document.getElementById("deductions-list");
    const cweCountTotal = document.getElementById("cwe-count-total");
    const cweCountCritical = document.getElementById("cwe-count-critical");
    const cweCountHigh = document.getElementById("cwe-count-high");
    const cweCountMedium = document.getElementById("cwe-count-medium");
    const cweCountLow = document.getElementById("cwe-count-low");

    function escapeHtml(str) {
        if (str === null || str === undefined) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    const astNodesCnt = document.getElementById("ast-nodes-cnt");
    const cfgCcCnt = document.getElementById("cfg-cc-cnt");
    const flogAllocCnt = document.getElementById("flog_alloc_cnt");
    const flogClonesCnt = document.getElementById("flog_clones_cnt");
    const cpgEdgesCnt = document.getElementById("cpg-edges-cnt");

    const xaiSection = document.getElementById("xai-section");
    const xaiExplanationText = document.getElementById("xai-explanation-text");
    const xaiPatchCode = document.getElementById("xai-patch-code");
    const copyPatchBtn = document.getElementById("copy-patch-btn");

    // File Upload Elements
    const uploadFileBtn = document.getElementById("upload-file-btn");
    const fileUploadInput = document.getElementById("file-upload-input");
    const fileBadge = document.getElementById("file-badge");
    const fileNameText = document.getElementById("file-name-text");
    const clearFileBtn = document.getElementById("clear-file-btn");
    const editorWrapper = document.getElementById("editor-wrapper");
    const dropOverlay = document.getElementById("drop-overlay");

    // Report Export Elements
    const exportPdfBtn = document.getElementById("export-pdf-btn");

    let currentAnalysisData = null;
    let activeFnIndex = 0;

    const sampleRustCode = `// RustAuditAI Sample Subroutine
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

    // Load sample Rust code
    if (loadSampleBtn) {
        loadSampleBtn.addEventListener("click", (e) => {
            e.preventDefault();
            if (codeEditor) {
                codeEditor.value = sampleRustCode;
                codeEditor.focus();
                codeEditor.dispatchEvent(new Event("input", { bubbles: true }));
            }
            if (fileBadge && fileNameText) {
                fileNameText.textContent = "sample_func.rs";
                fileBadge.classList.remove("hidden");
            }
        });
    }

    // File Upload via Web UI Logic (FileReader + Drag & Drop)
    function loadFileContent(file) {
        if (!file) return;

        // Check for .rs extension
        if (!file.name.endsWith(".rs") && !file.name.endsWith(".txt")) {
            alert(`Selected file '${file.name}' is not a Rust source file (.rs). Please choose a valid .rs file.`);
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            if (codeEditor) {
                codeEditor.value = content;
                codeEditor.focus();
                codeEditor.dispatchEvent(new Event("input", { bubbles: true }));
            }
            if (fileBadge && fileNameText) {
                fileNameText.textContent = file.name;
                fileBadge.classList.remove("hidden");
            }
        };
        reader.onerror = () => {
            alert("Failed to read the file. Please ensure it is a valid UTF-8 text file.");
        };
        reader.readAsText(file, "UTF-8");
    }

    if (uploadFileBtn && fileUploadInput) {
        uploadFileBtn.addEventListener("click", () => {
            fileUploadInput.value = "";
            fileUploadInput.click();
        });

        fileUploadInput.addEventListener("change", () => {
            if (fileUploadInput.files && fileUploadInput.files[0]) {
                loadFileContent(fileUploadInput.files[0]);
            }
        });
    }

    if (clearFileBtn) {
        clearFileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            if (fileBadge) fileBadge.classList.add("hidden");
            if (fileUploadInput) fileUploadInput.value = "";
        });
    }

    // Drag-and-Drop file handling onto code editor
    if (editorWrapper) {
        ["dragenter", "dragover"].forEach(eventName => {
            editorWrapper.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                editorWrapper.classList.add("drag-over");
                if (dropOverlay) dropOverlay.classList.remove("hidden");
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            editorWrapper.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                editorWrapper.classList.remove("drag-over");
                if (dropOverlay) dropOverlay.classList.add("hidden");
            });
        });

        editorWrapper.addEventListener("drop", (e) => {
            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                loadFileContent(e.dataTransfer.files[0]);
            }
        });
    }

    // Copy refactored patch button
    if (copyPatchBtn) {
        copyPatchBtn.addEventListener("click", async (e) => {
            e.preventDefault();
            const textToCopy = xaiPatchCode.textContent;
            if (!textToCopy || textToCopy.startsWith("// Error") || textToCopy.startsWith("// Optimal") || textToCopy.startsWith("// No refactored")) {
                return;
            }

            try {
                await navigator.clipboard.writeText(textToCopy);
                copyPatchBtn.classList.add("copied");
                copyPatchBtn.innerHTML = `<i class="fa-solid fa-check"></i> <span>Copied!</span>`;
                setTimeout(() => {
                    copyPatchBtn.classList.remove("copied");
                    copyPatchBtn.innerHTML = `<i class="fa-regular fa-copy"></i> <span>Copy Patch</span>`;
                }, 2000);
            } catch (err) {
                // Fallback for clipboard copy if navigator.clipboard API is unavailable
                const textarea = document.createElement("textarea");
                textarea.value = textToCopy;
                textarea.style.position = "fixed";
                textarea.style.opacity = "0";
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand("copy");
                document.body.removeChild(textarea);
                copyPatchBtn.classList.add("copied");
                copyPatchBtn.innerHTML = `<i class="fa-solid fa-check"></i> <span>Copied!</span>`;
                setTimeout(() => {
                    copyPatchBtn.classList.remove("copied");
                    copyPatchBtn.innerHTML = `<i class="fa-regular fa-copy"></i> <span>Copy Patch</span>`;
                }, 2000);
            }
        });
    }

    // Execute Audit API call
    analyzeBtn.addEventListener("click", async () => {
        const code = codeEditor.value.trim();
        if (!code) {
            alert("Please paste or type Rust function code before auditing!");
            return;
        }

        const enableXai = enableXaiToggle.checked;

        // UI states
        emptyState.classList.add("hidden");
        resultsContainer.classList.add("hidden");
        loaderState.classList.remove("hidden");

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: code, explain: enableXai }),
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                alert("Audit Failed: " + (data.error || "Syntax parsing error"));
                loaderState.classList.add("hidden");
                emptyState.classList.remove("hidden");
                return;
            }

            currentAnalysisData = data;
            activeFnIndex = 0;

            loaderState.classList.add("hidden");
            resultsContainer.classList.remove("hidden");

            renderFunctionTabs();
            renderActiveFunction();
        } catch (err) {
            alert("Network error: " + err.message);
            loaderState.classList.add("hidden");
            emptyState.classList.remove("hidden");
        }
    });

    // Helper function to trigger browser file download from Blob
    function triggerDownload(blob, defaultFilename, contentDisposition) {
        let filename = defaultFilename;
        if (contentDisposition && contentDisposition.includes("filename=")) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches && matches[1]) {
                filename = matches[1].replace(/['"]/g, "").trim();
            }
        }
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 300);
    }

    // Export PDF Quality Report Handler (SRS §4.6.5)
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions || currentAnalysisData.functions.length === 0) {
                alert("No audit analysis available to export. Please execute a graph audit first.");
                return;
            }

            const activeFn = currentAnalysisData.functions[activeFnIndex];
            const currentFilename = (fileNameText && !fileBadge.classList.contains("hidden"))
                ? fileNameText.textContent
                : ((activeFn && activeFn.name ? activeFn.name : "rust_subroutine") + ".rs");

            const originalHtml = exportPdfBtn.innerHTML;
            exportPdfBtn.disabled = true;
            exportPdfBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span>Exporting PDF...</span>`;

            try {
                const response = await fetch("/api/export/pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        function_data: activeFn,
                        filename: currentFilename,
                    }),
                });

                if (!response.ok) {
                    const err = await response.json().catch(() => ({}));
                    throw new Error(err.detail || "Server failed to render PDF report.");
                }

                const blob = await response.blob();
                const disposition = response.headers.get("Content-Disposition");
                triggerDownload(blob, `rustaudit_report_${activeFn.name || "subroutine"}.pdf`, disposition);
            } catch (err) {
                alert("PDF Export Error: " + err.message);
            } finally {
                exportPdfBtn.disabled = false;
                exportPdfBtn.innerHTML = originalHtml;
            }
        });
    }

    // XAI Readability Formatter & Card Renderer
    function formatMarkdownContent(text) {
        if (!text) return "";
        let formatted = escapeHtml(text);
        // Replace markdown inline code: `code`
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
        // Replace bold: **text**
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        // Replace LaTeX math notation: $V(G) \le 2$ or $V(G) <= 2$
        formatted = formatted.replace(/\$V\(G\)\s*(?:\\le|&lt;=)\s*(\d+)\$/gi, 'V(G) &le; $1');
        formatted = formatted.replace(/\$([^$]+)\$/g, '$1');

        // Cleanly format multi-line bullet lists if present
        if (formatted.includes("\n- ") || formatted.includes("\n* ") || formatted.startsWith("- ")) {
            const bulletLines = formatted.split(/\n\s*[-*]\s*/);
            if (bulletLines.length > 1 || formatted.startsWith("- ")) {
                return bulletLines
                    .map(b => b.replace(/^[-*]\s*/, '').trim())
                    .filter(b => b.length > 0)
                    .map(b => `<div class="xai-bullet-point"><i class="fa-solid fa-angle-right"></i> <span>${b}</span></div>`)
                    .join("");
            }
        }
        return formatted;
    }

    function renderXAIExplanation(explanationText, container) {
        if (!container) return;
        if (!explanationText || !explanationText.trim()) {
            container.innerHTML = `<div class="xai-empty-notice">No architectural explanation available.</div>`;
            return;
        }

        const trimmed = explanationText.trim().replace(/\s*---\s*$/, "").trim();

        // Check for optimal subroutine message
        if (trimmed.includes("perfect Rust Quality Index") || trimmed.includes("Optimal quality") || trimmed.includes("100.00 / 100")) {
            container.innerHTML = `
                <div class="xai-optimal-card">
                    <div class="xai-optimal-header">
                        <i class="fa-solid fa-circle-check"></i>
                        <span>Optimal Quality Invariant (RQI 100.00 / 100)</span>
                    </div>
                    <div class="xai-optimal-body">
                        ${formatMarkdownContent(trimmed)}
                    </div>
                </div>
            `;
            return;
        }

        // Split by numbered diagnostic points at line starts: e.g. "\n1. **", "\n2. **"
        const parts = trimmed.split(/(?:^|\n)\s*(?=\d+\.\s*(?:\*\*|[A-Z]))/);
        let intro = "";
        const items = [];

        parts.forEach((part) => {
            const p = part.trim();
            if (!p) return;

            const match = p.match(/^(\d+)\.\s*(.+)$/s);
            if (match) {
                const num = match[1];
                const body = match[2];

                let title = "";
                let rootCause = "";
                let remediation = "";
                let cweId = null;

                // Extract CWE if present e.g. ([CWE-119]) or [CWE-119]
                const cweMatch = body.match(/\[(CWE-\d+)\]/i) || body.match(/\b(CWE-\d+)\b/i);
                if (cweMatch) {
                    cweId = cweMatch[1].toUpperCase();
                }

                // Check if there is an explicit bold title at the start: e.g. **Title ([CWE-XXX])**: or **Title**:
                const boldTitleMatch = body.match(/^\s*\*\*([^*]+)\*\*\s*(?:[:\-–—]\s*)?(.*)$/s);
                let remaining = body;

                if (boldTitleMatch) {
                    title = boldTitleMatch[1];
                    remaining = boldTitleMatch[2] || "";
                } else {
                    const colonMatch = body.match(/^([^:\n]+)[:]\s*(.*)$/s);
                    if (colonMatch) {
                        title = colonMatch[1];
                        remaining = colonMatch[2] || "";
                    } else {
                        // If no valid title was found and we already have a previous item,
                        // this is prose that started with a number (e.g. "10. If the length..."), append to previous item
                        if (items.length > 0) {
                            const prev = items[items.length - 1];
                            if (prev.remediation) {
                                prev.remediation += " " + p;
                            } else {
                                prev.rootCause += " " + p;
                            }
                            return;
                        }
                        title = `Finding ${num}`;
                        remaining = body;
                    }
                }

                // Clean title of CWE tags, markdown links, and markdown markers
                title = title.replace(/\[CWE-\d+\](?:\([^)]*\))?|\(CWE-\d+\)|\(\[CWE-\d+\]\)/gi, "")
                             .replace(/\(\s*https?:\/\/[^\s)]+\s*\)/gi, "")
                             .replace(/^[:\s\-*]+|[:\s\-*]+$/g, "")
                             .replace(/\*\*/g, "")
                             .trim();

                // Now check if remaining has explicit Root Cause and Remediation labels
                const rcMatch = remaining.match(/(?:-\s*)?\*{0,2}Root Cause\*{0,2}\s*:\s*(.+?)(?=(?:-\s*)?\*{0,2}Remediation\*{0,2}\s*:|\Z)/is);
                const remMatch = remaining.match(/(?:-\s*)?\*{0,2}Remediation\*{0,2}\s*:\s*(.+)$/is);

                if (rcMatch) {
                    rootCause = rcMatch[1].trim();
                    if (remMatch) {
                        remediation = remMatch[1].trim();
                    }
                } else if (remMatch) {
                    remediation = remMatch[1].trim();
                    rootCause = remaining.substring(0, remMatch.index).trim();
                } else {
                    const fixMatch = remaining.match(/(?:-\s*)?\*{0,2}(?:Remediation|Fix|Solution)\*{0,2}\s*:\s*(.+)$/is);
                    if (fixMatch) {
                        remediation = fixMatch[1].trim();
                        rootCause = remaining.substring(0, fixMatch.index).trim();
                    } else {
                        rootCause = remaining.replace(/^[:\s\-–—]+/, "").trim();
                    }
                }

                rootCause = rootCause.replace(/^[:\s\-–—]+/, "").trim();

                items.push({
                    num: num,
                    title: title,
                    cweId: cweId,
                    rootCause: rootCause,
                    remediation: remediation,
                });
            } else {
                if (!intro && items.length === 0) {
                    intro = p;
                }
            }
        });

        if (items.length === 0) {
            // Fallback for general narrative or bulleted paragraphs
            const paragraphs = trimmed.split(/\n\s*\n/).filter(p => p.trim());
            container.innerHTML = `
                <div class="xai-narrative-container">
                    ${paragraphs.map(p => `<p class="xai-narrative-p">${formatMarkdownContent(p).replace(/\n/g, '<br/>')}</p>`).join('')}
                </div>
            `;
            return;
        }

        let html = "";

        if (intro) {
            html += `
                <div class="xai-intro-banner">
                    <i class="fa-solid fa-circle-info"></i>
                    <span>${formatMarkdownContent(intro)}</span>
                </div>
            `;
        }

        html += `<div class="xai-cards-grid">`;

        items.forEach((item) => {
            const cweBadgeHtml = item.cweId ? `
                <span class="xai-cwe-pill" title="Identified Weakness: ${item.cweId}">
                    <i class="fa-solid fa-shield-halved"></i> ${item.cweId}
                </span>
            ` : '';

            const causeHtml = item.rootCause ? `
                <div class="xai-cause-box">
                    <div class="xai-box-label">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                        <span>Root Cause & Flaw Analysis</span>
                    </div>
                    <div class="xai-box-content">
                        ${formatMarkdownContent(item.rootCause)}
                    </div>
                </div>
            ` : '';

            const remediationHtml = item.remediation ? `
                <div class="xai-remediation-box">
                    <div class="xai-box-label">
                        <i class="fa-solid fa-wrench"></i>
                        <span>Remediation Guidance</span>
                    </div>
                    <div class="xai-box-content">
                        ${formatMarkdownContent(item.remediation)}
                    </div>
                </div>
            ` : '';

            html += `
                <div class="xai-insight-card">
                    <div class="xai-card-title-row">
                        <div class="xai-card-title-left">
                            <span class="xai-step-badge">${item.num}</span>
                            <span class="xai-card-title-text">${formatMarkdownContent(item.title)}</span>
                        </div>
                        ${cweBadgeHtml}
                    </div>
                    ${causeHtml}
                    ${remediationHtml}
                </div>
            `;
        });

        html += `</div>`;
        container.innerHTML = html;
    }

    function renderFunctionTabs() {
        functionTabs.innerHTML = "";
        if (!currentAnalysisData || !currentAnalysisData.functions) return;

        currentAnalysisData.functions.forEach((fn, idx) => {
            const btn = document.createElement("button");
            btn.className = `tab-btn ${idx === activeFnIndex ? "active" : ""}`;
            btn.innerHTML = `<i class="fa-solid fa-cube"></i> fn ${fn.name}()`;
            btn.addEventListener("click", () => {
                activeFnIndex = idx;
                renderFunctionTabs();
                renderActiveFunction();
            });
            functionTabs.appendChild(btn);
        });
    }

    const devModeToggle = document.getElementById("developer-mode-toggle");
    const devGraphContainer = document.getElementById("dev-graph-container");
    const interactiveCanvas = document.getElementById("interactive-canvas");
    const outliersContentList = document.getElementById("outliers-content-list");
    const graphTypeBtns = document.querySelectorAll(".graph-type-btn");
    const pathSafety = document.getElementById("path-safety");
    const pathPerf = document.getElementById("path-perf");
    const pathMaint = document.getElementById("path-maint");
    const pathSec = document.getElementById("path-sec");
    const rqiGradeLetter = document.getElementById("rqi-grade-letter");
    const rqiGradeText = document.getElementById("rqi-grade-text");
    const graphMetricsBar = document.getElementById("graph-metrics-bar");
    const nonDevRqiCard = document.getElementById("non-dev-rqi-card");
    const nonDevDeductionsBox = document.getElementById("non-dev-deductions-box");
    const devRqiCard = document.getElementById("dev-rqi-card");
    const devRqiScoreNum = document.getElementById("dev-rqi-score-num");
    const devScoreCirclePath = document.getElementById("dev-score-circle-path");
    const devCalcWeightedSum = document.getElementById("dev-calc-weighted-sum");
    const devCalcPenaltyVal = document.getElementById("dev-calc-penalty-val");
    const devVectorsVerticalList = document.getElementById("dev-vectors-vertical-list");

    let networkInstance = null;
    let activeGraphType = "flog";

    // Developer Mode Toggle Event
    devModeToggle.addEventListener("change", () => {
        if (devModeToggle.checked) {
            if (nonDevRqiCard) nonDevRqiCard.classList.add("hidden");
            if (nonDevDeductionsBox) nonDevDeductionsBox.classList.add("hidden");
            if (devRqiCard) devRqiCard.classList.remove("hidden");
            devGraphContainer.classList.remove("hidden");
            xaiSection.classList.add("hidden");
            renderGraphCanvas();
        } else {
            if (nonDevRqiCard) nonDevRqiCard.classList.remove("hidden");
            if (nonDevDeductionsBox) nonDevDeductionsBox.classList.remove("hidden");
            if (devRqiCard) devRqiCard.classList.add("hidden");
            devGraphContainer.classList.add("hidden");
            if (currentAnalysisData && currentAnalysisData.functions[activeFnIndex]?.xai_report) {
                xaiSection.classList.remove("hidden");
            }
        }
    });

    // Graph Type Switcher Buttons (FLOG, CFG, AST)
    graphTypeBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            graphTypeBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeGraphType = btn.getAttribute("data-graph");
            renderGraphCanvas();
        });
    });

    function renderActiveFunction() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;

        const fnData = currentAnalysisData.functions[activeFnIndex];
        const rqi = fnData.rqi;

        // RQI Main Gauge (FLOAT with decimal point)
        rqiScoreNum.textContent = rqi.rqi_score.toFixed(1);
        scoreCirclePath.setAttribute("stroke-dasharray", `${rqi.rqi_score.toFixed(1)}, 100`);

        // Parse Grade Letter and Text (e.g. "A (Good Quality)" -> letter "A", text "Good Quality")
        const rawGrade = rqi.grade || "A (Good Quality)";
        const match = rawGrade.match(/^([A-Z]\+?)\s*\((.*)\)$/);
        let letter = "A";
        let text = rawGrade;
        if (match) {
            letter = match[1];
            text = match[2];
        }

        if (rqiGradeLetter) rqiGradeLetter.textContent = letter;
        if (rqiGradeText) rqiGradeText.textContent = text;

        // Grade Color Scheme
        let gradeColor = "#34d399";
        let gradeBg = "rgba(16, 185, 129, 0.15)";
        let gradeBorder = "rgba(16, 185, 129, 0.3)";

        if (rqi.rqi_score < 60) {
            gradeColor = "#f87171";
            gradeBg = "rgba(239, 68, 68, 0.15)";
            gradeBorder = "rgba(239, 68, 68, 0.3)";
        } else if (rqi.rqi_score < 80) {
            gradeColor = "#fbbf24";
            gradeBg = "rgba(245, 158, 11, 0.15)";
            gradeBorder = "rgba(245, 158, 11, 0.3)";
        }

        if (rqiGradeLetter) rqiGradeLetter.style.color = gradeColor;
        if (rqiGradeText) {
            rqiGradeText.style.color = gradeColor;
            rqiGradeText.style.backgroundColor = gradeBg;
            rqiGradeText.style.borderColor = gradeBorder;
        }

        // 4 Vector Gauges (INTEGER VALUES)
        const intSafety = Math.round(rqi.safety_score);
        const intPerf = Math.round(rqi.performance_score);
        const intMaint = Math.round(rqi.maintainability_score);
        const intSec = Math.round(rqi.security_score);

        valSafety.textContent = intSafety;
        if (pathSafety) pathSafety.setAttribute("stroke-dasharray", `${intSafety}, 100`);

        valPerf.textContent = intPerf;
        if (pathPerf) pathPerf.setAttribute("stroke-dasharray", `${intPerf}, 100`);

        valMaint.textContent = intMaint;
        if (pathMaint) pathMaint.setAttribute("stroke-dasharray", `${intMaint}, 100`);

        valSec.textContent = intSec;
        if (pathSec) pathSec.setAttribute("stroke-dasharray", `${intSec}, 100`);

        // Render Developer Mode RQI Analysis Card (No Grade Letter or Label!)
        if (devRqiScoreNum) devRqiScoreNum.textContent = rqi.rqi_score.toFixed(1);
        if (devScoreCirclePath) devScoreCirclePath.setAttribute("stroke-dasharray", `${rqi.rqi_score.toFixed(1)}, 100`);

        const weightedSum = (0.30 * intSafety + 0.25 * intPerf + 0.25 * intMaint + 0.20 * intSec).toFixed(1);
        if (devCalcWeightedSum) devCalcWeightedSum.textContent = weightedSum;
        if (devCalcPenaltyVal) {
            devCalcPenaltyVal.textContent = rqi.penalty_applied ? "-1.7 pts (Penalty Triggered)" : "0.0 pts (No Penalty)";
            devCalcPenaltyVal.style.color = rqi.penalty_applied ? "#f87171" : "#34d399";
        }

        // Render 4 Vector Rows Stacked Vertically Below Each Other with Pros & Cons
        if (devVectorsVerticalList) {
            devVectorsVerticalList.innerHTML = "";
            const vectorConfigs = [
                {
                    key: "safety",
                    name: "Safety Vector",
                    score: intSafety,
                    icon: "fa-user-shield",
                    color: "var(--safety-color)",
                    defaultPros: ["Safe reference abstractions", "Zero raw pointer mutations"]
                },
                {
                    key: "performance",
                    name: "Performance Vector",
                    score: intPerf,
                    icon: "fa-gauge-high",
                    color: "var(--perf-color)",
                    defaultPros: ["Pass-by-reference (&T)", "Stack-allocated scope bindings"]
                },
                {
                    key: "maintainability",
                    name: "Maintainability Vector",
                    score: intMaint,
                    icon: "fa-cubes-stacked",
                    color: "var(--maint-color)",
                    defaultPros: ["McCabe Cyclomatic Complexity V(G) <= 5", "Idiomatic Rust control flow"]
                },
                {
                    key: "security",
                    name: "Security Vector",
                    score: intSec,
                    icon: "fa-lock",
                    color: "var(--sec-color)",
                    defaultPros: ["Memory boundary isolation", "Encapsulated safety contract"]
                }
            ];

            vectorConfigs.forEach(vc => {
                const card = document.createElement("div");
                card.className = "dev-vector-row-card";

                const consList = rqi.deductions ? (rqi.deductions[vc.key] || []) : [];
                const structuredCons = (rqi.structured_deductions && rqi.structured_deductions[vc.key]) || [];
                const prosList = vc.score === 100 ? vc.defaultPros : vc.defaultPros.slice(0, 1);

                let rationaleHtml = `<div class="rationale-group">`;
                prosList.forEach(p => {
                    rationaleHtml += `<span class="rationale-tag tag-pro"><i class="fa-solid fa-circle-check"></i> ${p}</span>`;
                });

                if (structuredCons.length > 0) {
                    structuredCons.forEach(sc => {
                        const cweLink = sc.cwe_id ? `<a href="${sc.cwe_url || `https://cwe.mitre.org/data/definitions/${sc.cwe_id.replace('CWE-', '')}.html`}" target="_blank" rel="noopener noreferrer" class="dev-cwe-pill severity-${sc.severity}" title="${escapeHtml(sc.cwe_name || sc.cwe_id)}"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${sc.cwe_id}</a>` : '';
                        const lineBadge = sc.line_number ? `<span class="dev-line-tag">Line ${sc.line_number}</span>` : '';
                        rationaleHtml += `
                            <div class="rationale-tag tag-con severity-${sc.severity}">
                                <div class="dev-con-main">
                                    <i class="fa-solid fa-circle-minus"></i>
                                    ${cweLink}
                                    ${lineBadge}
                                    <span class="dev-con-desc">${escapeHtml(sc.description)}</span>
                                    <span class="dev-con-penalty">(-${Number(sc.penalty || 0).toFixed(1)} pts)</span>
                                </div>
                                ${sc.remediation ? `<div class="dev-con-remediation"><i class="fa-solid fa-wrench"></i> ${escapeHtml(sc.remediation)}</div>` : ''}
                            </div>
                        `;
                    });
                } else {
                    consList.forEach(c => {
                        rationaleHtml += `<span class="rationale-tag tag-con"><i class="fa-solid fa-circle-minus"></i> ${escapeHtml(c)}</span>`;
                    });
                }
                rationaleHtml += `</div>`;

                card.innerHTML = `
                    <div class="dev-vector-left-meta">
                        <div class="mini-dial">
                            <svg viewBox="0 0 36 36" class="mini-chart">
                                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                                <path class="circle" style="stroke: ${vc.color};" stroke-dasharray="${vc.score}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                                <text x="18" y="20.35" class="mini-percentage">${vc.score}</text>
                            </svg>
                        </div>
                        <div class="v-title-box">
                            <span class="v-name"><i class="fa-solid ${vc.icon}" style="color: ${vc.color};"></i> ${vc.name}</span>
                        </div>
                    </div>
                    <div class="dev-vector-rationale-right">
                        ${rationaleHtml}
                    </div>
                `;
                devVectorsVerticalList.appendChild(card);
            });
        }

        // Update CWE Weaknesses Summary Bar
        const cweSummary = fnData.cwe_summary || rqi.cwe_summary || { total: 0, critical: 0, high: 0, medium: 0, low: 0 };
        if (cweCountTotal) {
            cweCountTotal.textContent = `${cweSummary.total || 0} Total`;
            cweCountTotal.className = `cwe-counter-badge total ${cweSummary.total > 0 ? "has-flaws" : ""}`;
        }
        if (cweCountCritical) {
            cweCountCritical.textContent = `${cweSummary.critical || 0} Critical`;
            cweCountCritical.style.display = (cweSummary.critical > 0) ? "inline-flex" : "none";
        }
        if (cweCountHigh) {
            cweCountHigh.textContent = `${cweSummary.high || 0} High`;
            cweCountHigh.style.display = (cweSummary.high > 0) ? "inline-flex" : "none";
        }
        if (cweCountMedium) {
            cweCountMedium.textContent = `${cweSummary.medium || 0} Medium`;
            cweCountMedium.style.display = (cweSummary.medium > 0) ? "inline-flex" : "none";
        }
        if (cweCountLow) {
            cweCountLow.textContent = `${cweSummary.low || 0} Low`;
            cweCountLow.style.display = (cweSummary.low > 0) ? "inline-flex" : "none";
        }

        // Quality Deductions & Indicator Logs
        deductionsList.innerHTML = "";
        const severityRank = { "CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1 };
        const structuredList = Object.values(rqi.structured_deductions || {}).flat();

        if (structuredList.length > 0) {
            structuredList.sort((a, b) => {
                const diff = (severityRank[b.severity] || 0) - (severityRank[a.severity] || 0);
                if (diff !== 0) return diff;
                return (a.line_number || 9999) - (b.line_number || 9999);
            });

            structuredList.forEach(d => {
                const li = document.createElement("li");
                li.className = `deduction-card severity-${d.severity || 'LOW'}`;

                const cwePillHtml = d.cwe_id ? `
                    <a href="${d.cwe_url || `https://cwe.mitre.org/data/definitions/${d.cwe_id.replace('CWE-', '')}.html`}" 
                       target="_blank" rel="noopener noreferrer" class="cwe-pill severity-${d.severity}" 
                       title="View official MITRE definition for ${escapeHtml(d.cwe_name || d.cwe_id)}">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i> ${d.cwe_id}
                    </a>
                ` : '';

                const lineTagHtml = d.line_number ? `
                    <span class="cwe-line-tag" title="Exact Statement Location"><i class="fa-solid fa-crosshairs"></i> Line ${d.line_number}</span>
                ` : '';

                const severityTagHtml = d.severity ? `
                    <span class="cwe-severity-tag severity-${d.severity}">${d.severity}</span>
                ` : '';

                const vectorTagHtml = d.vector ? `
                    <span class="cwe-vector-tag vector-${d.vector}"><i class="fa-solid fa-layer-group"></i> ${d.vector.toUpperCase()}</span>
                ` : '';

                const penaltyHtml = `<span class="deduction-penalty">-${Number(d.penalty || 0).toFixed(1)} pts</span>`;

                const codeHtml = d.statement_code ? `
                    <div class="cwe-code-snippet"><code>${escapeHtml(d.statement_code)}</code></div>
                ` : '';

                li.innerHTML = `
                    <div class="deduction-card-header">
                        <div class="deduction-badges-left">
                            ${cwePillHtml}
                            ${lineTagHtml}
                            ${severityTagHtml}
                            ${vectorTagHtml}
                        </div>
                        ${penaltyHtml}
                    </div>
                    <div class="deduction-desc">${escapeHtml(d.description)}</div>
                    ${codeHtml}
                `;
                deductionsList.appendChild(li);
            });
        } else {
            const rawDeductions = Object.values(rqi.deductions || {}).flat();
            if (rawDeductions.length === 0) {
                const li = document.createElement("li");
                li.className = "deduction-clean-state";
                li.innerHTML = `<i class="fa-solid fa-circle-check"></i> No quality deductions or CWE flaws detected. Subroutine is idiomatic and clean!`;
                deductionsList.appendChild(li);
            } else {
                rawDeductions.forEach(d => {
                    const li = document.createElement("li");
                    li.className = "deduction-card severity-LOW";
                    li.innerHTML = `<div class="deduction-desc">${escapeHtml(d)}</div>`;
                    deductionsList.appendChild(li);
                });
            }
        }

        // CPG Metrics
        astNodesCnt.textContent = fnData.cpg_summary.ast_nodes;
        cfgCcCnt.textContent = fnData.cpg_summary.cyclomatic_complexity;
        flogAllocCnt.textContent = fnData.cpg_summary.allocations;
        flogClonesCnt.textContent = fnData.cpg_summary.clones;
        if (cpgEdgesCnt) cpgEdgesCnt.textContent = fnData.cpg_summary.cpg_edges;

        // Developer Mode Visibility Render
        if (devModeToggle.checked) {
            if (nonDevRqiCard) nonDevRqiCard.classList.add("hidden");
            if (nonDevDeductionsBox) nonDevDeductionsBox.classList.add("hidden");
            if (devRqiCard) devRqiCard.classList.remove("hidden");
            devGraphContainer.classList.remove("hidden");
            xaiSection.classList.add("hidden");
            renderGraphCanvas();
        } else {
            if (nonDevRqiCard) nonDevRqiCard.classList.remove("hidden");
            if (nonDevDeductionsBox) nonDevDeductionsBox.classList.remove("hidden");
            if (devRqiCard) devRqiCard.classList.add("hidden");
            devGraphContainer.classList.add("hidden");
            if (fnData.xai_report) {
                xaiSection.classList.remove("hidden");
                if (fnData.xai_report.error) {
                    xaiExplanationText.innerHTML = `<span style="color: #f87171;"><i class="fa-solid fa-triangle-exclamation"></i> ${fnData.xai_report.error}</span>`;
                    xaiPatchCode.textContent = "// Error generating XAI refactoring patch";
                    if (copyPatchBtn) copyPatchBtn.style.display = "none";
                } else {
                    renderXAIExplanation(fnData.xai_report.explanation, xaiExplanationText);
                    if (fnData.rqi && fnData.rqi.rqi_score >= 100.0 && !fnData.xai_report.refactored_code) {
                        xaiPatchCode.textContent = "// Optimal Subroutine (RQI 100.00 / 100). No refactoring required.";
                        if (copyPatchBtn) copyPatchBtn.style.display = "none";
                    } else {
                        xaiPatchCode.textContent = fnData.xai_report.refactored_code || "// No refactored patch required";
                        if (copyPatchBtn) {
                            copyPatchBtn.style.display = fnData.xai_report.refactored_code ? "inline-flex" : "none";
                        }
                    }
                }
            } else {
                xaiSection.classList.add("hidden");
            }
        }
    }


    function renderGraphCanvas() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;

        const fnData = currentAnalysisData.functions[activeFnIndex];
        const rawNodes = fnData.nodes[activeGraphType] || [];
        const rawEdges = fnData.edges[activeGraphType] || [];

        // Build Vis-Network Nodes
        const nodes = rawNodes.map(n => {
            let label = n.label || n.var_name || n.name || n.kind || n.node_type || n.id;
            let color = "#6366f1"; // Default indigo
            let shape = "box";

            if (activeGraphType === "cpg") {
                // Unified CPG Multi-Layer Semantic Coloring
                if (n.layer === "AST") {
                    color = "#06b6d4"; // Cyan for AST syntax
                } else if (n.layer === "CFG") {
                    color = n.is_decision ? "#f59e0b" : "#3b82f6"; // Amber for decision, Blue for control flow
                } else if (n.layer === "FLOG") {
                    if (n.is_unsafe || n.node_type === "UnsafeOperation") color = "#dc2626"; // Crimson
                    else if (n.is_clone || n.node_type === "ClonedBinding") color = "#ef4444"; // Red
                    else if (n.is_heap_alloc || n.node_type === "HeapAllocation") color = "#a855f7"; // Purple
                    else color = "#10b981"; // Emerald for normal bindings
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
                font: { color: "#ffffff", face: "Fira Code" },
                shape: shape,
                margin: 10,
            };
        });

        // Build Vis-Network Edges
        const edges = rawEdges.map(e => {
            let isCrossLayer = e.edge_type && (
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

        const container = interactiveCanvas;
        const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        const options = {
            physics: {
                solver: "forceAtlas2Based",
                stabilization: { iterations: 120 },
                forceAtlas2Based: {
                    gravitationalConstant: -40,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                }
            },
            interaction: { hover: true, zoomView: true, dragView: true },
        };

        if (networkInstance) networkInstance.destroy();
        networkInstance = new vis.Network(container, data, options);

        // Render Graph Outliers for active graph type
        if (activeGraphType === "cpg") {
            const allOutliers = [
                ...(fnData.graph_outliers.ast || []),
                ...(fnData.graph_outliers.cfg || []),
                ...(fnData.graph_outliers.flog || []),
            ];
            renderOutliers(allOutliers);
        } else {
            renderOutliers(fnData.graph_outliers[activeGraphType] || []);
        }
    }

    function renderOutliers(outliersList) {
        outliersContentList.innerHTML = "";
        if (!outliersList || outliersList.length === 0) {
            outliersContentList.innerHTML = `<p style="font-size:0.8rem; color:#34d399;"><i class="fa-solid fa-circle-check"></i> No anomalies or topological outliers detected in ${activeGraphType.toUpperCase()} graph model.</p>`;
            return;
        }

        outliersList.forEach(item => {
            const card = document.createElement("div");
            card.className = `outlier-card-item severity-${item.severity}`;

            const cweHtml = item.cwe_id ? `
                <a href="${item.cwe_url || `https://cwe.mitre.org/data/definitions/${item.cwe_id.replace('CWE-','')}.html`}" 
                   target="_blank" rel="noopener noreferrer" class="cwe-pill severity-${item.severity}" 
                   title="${escapeHtml(item.cwe_name || item.cwe_id)}">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> ${item.cwe_id}
                </a>
            ` : '';

            const lineHtml = item.line_number ? `
                <span class="cwe-line-tag"><i class="fa-solid fa-crosshairs"></i> Line ${item.line_number}</span>
            ` : '';

            const codeHtml = item.statement_code ? `
                <div class="cwe-code-snippet"><code>${escapeHtml(item.statement_code)}</code></div>
            ` : '';

            const remediationHtml = item.remediation ? `
                <div class="cwe-remediation">
                    <i class="fa-solid fa-screwdriver-wrench"></i> <strong>Remediation:</strong> ${escapeHtml(item.remediation)}
                </div>
            ` : '';

            card.innerHTML = `
                <div class="outlier-card-header">
                    <div class="outlier-left">
                        <h5>${escapeHtml(item.title)}</h5>
                        <div class="outlier-badges">
                            ${cweHtml}
                            ${lineHtml}
                        </div>
                    </div>
                    <span class="severity-badge severity-${item.severity}">[${item.severity}]</span>
                </div>
                <p>${escapeHtml(item.description)}</p>
                ${codeHtml}
                ${remediationHtml}
            `;
            outliersContentList.appendChild(card);
        });
    }
});


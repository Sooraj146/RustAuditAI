/**
 * RustAuditAI Web Dashboard Client Logic (Unstyled / Functional)
 * Master design blueprint archived in UI_DASHBOARD_COMPONENTS.md
 */

document.addEventListener("DOMContentLoaded", () => {
    const codeEditor = document.getElementById("code-editor");
    const loadSampleBtn = document.getElementById("load-sample-btn");
    const analyzeBtn = document.getElementById("analyze-btn");
    const enableXaiToggle = document.getElementById("enable-xai-toggle");
    const devModeToggle = document.getElementById("developer-mode-toggle");

    const emptyState = document.getElementById("welcome-empty-state");
    const loaderState = document.getElementById("loader-state");
    const resultsContainer = document.getElementById("audit-results-container");

    const functionTabs = document.getElementById("function-tabs");
    const rqiScoreNum = document.getElementById("rqi-score-num");
    const rqiGradeLetter = document.getElementById("rqi-grade-letter");
    const rqiGradeText = document.getElementById("rqi-grade-text");

    const valSafety = document.getElementById("val-safety");
    const valPerf = document.getElementById("val-perf");
    const valMaint = document.getElementById("val-maint");
    const valSec = document.getElementById("val-sec");

    const deductionsList = document.getElementById("deductions-list");
    const cweCountTotal = document.getElementById("cwe-count-total");
    const cweCountCritical = document.getElementById("cwe-count-critical");
    const cweCountHigh = document.getElementById("cwe-count-high");
    const cweCountMedium = document.getElementById("cwe-count-medium");
    const cweCountLow = document.getElementById("cwe-count-low");

    const devRqiCard = document.getElementById("dev-rqi-card");
    const devRqiScoreNum = document.getElementById("dev-rqi-score-num");
    const devCalcWeightedSum = document.getElementById("dev-calc-weighted-sum");
    const devCalcPenaltyVal = document.getElementById("dev-calc-penalty-val");
    const devVectorsList = document.getElementById("dev-vectors-vertical-list");
    const devGraphContainer = document.getElementById("dev-graph-container");
    const interactiveCanvas = document.getElementById("interactive-canvas");

    const astNodesCnt = document.getElementById("ast-nodes-cnt");
    const cfgCcCnt = document.getElementById("cfg-cc-cnt");
    const flogAllocCnt = document.getElementById("flog_alloc_cnt");
    const flogClonesCnt = document.getElementById("flog_clones_cnt");
    const cpgEdgesCnt = document.getElementById("cpg-edges-cnt");
    const outliersContentList = document.getElementById("outliers-content-list");

    const xaiSection = document.getElementById("xai-section");
    const xaiExplanationText = document.getElementById("xai-explanation-text");
    const xaiPatchCode = document.getElementById("xai-patch-code");
    const copyPatchBtn = document.getElementById("copy-patch-btn");
    const applyPatchBtn = document.getElementById("apply-patch-btn");

    // Revisions
    const revisionsToggleBtn = document.getElementById("revisions-toggle-btn");
    const revCountBadge = document.getElementById("rev-count-badge");
    const revisionDrawerOverlay = document.getElementById("revision-drawer-overlay");
    const revisionHistoryDrawer = document.getElementById("revision-history-drawer");
    const closeDrawerBtn = document.getElementById("close-drawer-btn");
    const drawerFnSubtitle = document.getElementById("drawer-fn-subtitle");
    const revisionsTimelineContainer = document.getElementById("revisions-timeline-container");
    const revisionsEmptyState = document.getElementById("revisions-empty-state");
    const clearRevisionsBtn = document.getElementById("clear-revisions-btn");

    // Upload
    const uploadFileBtn = document.getElementById("upload-file-btn");
    const fileUploadInput = document.getElementById("file-upload-input");
    const fileBadge = document.getElementById("file-badge");
    const fileNameText = document.getElementById("file-name-text");
    const clearFileBtn = document.getElementById("clear-file-btn");
    const editorWrapper = document.getElementById("editor-wrapper");
    const dropOverlay = document.getElementById("drop-overlay");

    // Export
    const exportPdfBtn = document.getElementById("export-pdf-btn");

    let currentAnalysisData = null;
    let activeFnIndex = 0;
    let activeGraphType = "flog";
    let networkInstance = null;

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

    // Sample Loader
    if (loadSampleBtn) {
        loadSampleBtn.addEventListener("click", () => {
            if (codeEditor) {
                codeEditor.value = sampleRustCode;
            }
            if (fileBadge && fileNameText) {
                fileNameText.textContent = "sample_func.rs";
                fileBadge.style.display = "inline";
            }
        });
    }

    // File Upload Handler
    function handleFile(file) {
        if (!file) return;
        if (!file.name.endsWith(".rs") && !file.name.endsWith(".txt")) {
            alert("Please select a valid Rust (.rs) file.");
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
            if (codeEditor) codeEditor.value = e.target.result;
            if (fileBadge && fileNameText) {
                fileNameText.textContent = file.name;
                fileBadge.style.display = "inline";
            }
        };
        reader.readAsText(file);
    }

    if (uploadFileBtn && fileUploadInput) {
        uploadFileBtn.addEventListener("click", () => fileUploadInput.click());
        fileUploadInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) handleFile(e.target.files[0]);
        });
    }

    if (clearFileBtn) {
        clearFileBtn.addEventListener("click", () => {
            if (fileUploadInput) fileUploadInput.value = "";
            if (fileBadge) fileBadge.style.display = "none";
        });
    }

    // Drag and Drop
    if (editorWrapper) {
        editorWrapper.addEventListener("dragover", (e) => {
            e.preventDefault();
            if (dropOverlay) dropOverlay.style.display = "block";
        });
        editorWrapper.addEventListener("dragleave", (e) => {
            e.preventDefault();
            if (dropOverlay) dropOverlay.style.display = "none";
        });
        editorWrapper.addEventListener("drop", (e) => {
            e.preventDefault();
            if (dropOverlay) dropOverlay.style.display = "none";
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFile(e.dataTransfer.files[0]);
            }
        });
    }

    // Execute Audit
    if (analyzeBtn) {
        analyzeBtn.addEventListener("click", async () => {
            const code = codeEditor ? codeEditor.value.trim() : "";
            if (!code) {
                alert("Please enter or upload Rust code to analyze.");
                return;
            }

            if (emptyState) emptyState.style.display = "none";
            if (resultsContainer) resultsContainer.style.display = "none";
            if (loaderState) loaderState.style.display = "block";

            try {
                const res = await fetch("/api/analyze", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        code: code,
                        explain: enableXaiToggle ? enableXaiToggle.checked : true,
                    }),
                });

                const data = await res.json();
                if (!res.ok || !data.success) {
                    alert("Audit Failed: " + (data.error || "Syntax parsing error"));
                    if (loaderState) loaderState.style.display = "none";
                    if (emptyState) emptyState.style.display = "block";
                    return;
                }

                currentAnalysisData = data;
                activeFnIndex = 0;

                if (loaderState) loaderState.style.display = "none";
                if (resultsContainer) resultsContainer.style.display = "block";

                renderFunctionTabs();
                renderActiveFunction();
            } catch (err) {
                alert("Network error: " + err.message);
                if (loaderState) loaderState.style.display = "none";
                if (emptyState) emptyState.style.display = "block";
            }
        });
    }

    // Subroutine Tabs
    function renderFunctionTabs() {
        if (!functionTabs || !currentAnalysisData) return;
        functionTabs.innerHTML = "";
        const fns = currentAnalysisData.functions || [];
        fns.forEach((fn, idx) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.textContent = `fn ${fn.name}() (RQI: ${fn.rqi ? fn.rqi.rqi_score.toFixed(1) : 'N/A'})`;
            btn.style.marginRight = "8px";
            if (idx === activeFnIndex) btn.style.fontWeight = "bold";
            btn.addEventListener("click", () => {
                activeFnIndex = idx;
                renderFunctionTabs();
                renderActiveFunction();
            });
            functionTabs.appendChild(btn);
        });
    }

    // Render Active Subroutine
    function renderActiveFunction() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
        const fnData = currentAnalysisData.functions[activeFnIndex];
        const rqi = fnData.rqi || {};

        if (rqiScoreNum) rqiScoreNum.textContent = rqi.rqi_score !== undefined ? rqi.rqi_score.toFixed(1) : "0";
        if (devRqiScoreNum) devRqiScoreNum.textContent = rqi.rqi_score !== undefined ? rqi.rqi_score.toFixed(1) : "0";

        if (rqiGradeLetter && rqi.grade) {
            const match = rqi.grade.match(/^([A-Z]\+?)\s*\((.*)\)$/);
            rqiGradeLetter.textContent = match ? match[1] : rqi.grade;
            if (rqiGradeText) rqiGradeText.textContent = match ? match[2] : "";
        }

        if (valSafety) valSafety.textContent = rqi.safety_score !== undefined ? rqi.safety_score.toFixed(1) : "0";
        if (valPerf) valPerf.textContent = rqi.performance_score !== undefined ? rqi.performance_score.toFixed(1) : "0";
        if (valMaint) valMaint.textContent = rqi.maintainability_score !== undefined ? rqi.maintainability_score.toFixed(1) : "0";
        if (valSec) valSec.textContent = rqi.security_score !== undefined ? rqi.security_score.toFixed(1) : "0";

        // CWE counts
        const cwe = fnData.cwe_summary || {};
        if (cweCountTotal) cweCountTotal.textContent = `${cwe.total || 0} Total`;
        if (cweCountCritical) cweCountCritical.textContent = `${cwe.critical || 0} Critical`;
        if (cweCountHigh) cweCountHigh.textContent = `${cwe.high || 0} High`;
        if (cweCountMedium) cweCountMedium.textContent = `${cwe.medium || 0} Medium`;
        if (cweCountLow) cweCountLow.textContent = `${cwe.low || 0} Low`;

        // Deductions list
        if (deductionsList) {
            deductionsList.innerHTML = "";
            const structured = (rqi.structured_deductions_list || []);
            if (structured.length === 0) {
                deductionsList.innerHTML = "<li>No quality deductions. Code is optimal!</li>";
            } else {
                structured.forEach(d => {
                    const li = document.createElement("li");
                    li.textContent = `[${d.vector.toUpperCase()}] [${d.cwe_id || 'N/A'}] Line ${d.line_number || '-'}: ${d.message} (-${d.penalty} pts)`;
                    deductionsList.appendChild(li);
                });
            }
        }

        // Developer mode formula
        if (devCalcWeightedSum) {
            const sum = 0.3 * (rqi.safety_score || 0) + 0.25 * (rqi.performance_score || 0) + 0.25 * (rqi.maintainability_score || 0) + 0.2 * (rqi.security_score || 0);
            devCalcWeightedSum.textContent = sum.toFixed(1);
        }
        if (devCalcPenaltyVal) {
            devCalcPenaltyVal.textContent = rqi.penalty_applied ? rqi.penalty_reasons.join("; ") : "None";
        }

        // Graph stats
        const cpgSum = fnData.cpg_summary || {};
        if (astNodesCnt) astNodesCnt.textContent = cpgSum.ast_nodes || 0;
        if (cfgCcCnt) cfgCcCnt.textContent = cpgSum.cyclomatic_complexity || 1;
        if (flogAllocCnt) flogAllocCnt.textContent = cpgSum.allocations || 0;
        if (flogClonesCnt) flogClonesCnt.textContent = cpgSum.clones || 0;
        if (cpgEdgesCnt) cpgEdgesCnt.textContent = cpgSum.cpg_edges || 0;

        // XAI Section
        if (fnData.xai_report && xaiSection) {
            xaiSection.style.display = "block";
            if (xaiExplanationText) xaiExplanationText.textContent = fnData.xai_report.explanation || "";
            if (xaiPatchCode) xaiPatchCode.textContent = fnData.xai_report.refactored_code || "// No refactored patch required";
        }

        // Revisions badge
        if (revCountBadge) {
            revCountBadge.textContent = fnData.total_revisions || (fnData.revisions ? fnData.revisions.length : 0);
        }

        updateModeVisibility();
    }

    // Toggle Dev Mode
    function updateModeVisibility() {
        const isDev = devModeToggle && devModeToggle.checked;
        if (devRqiCard) devRqiCard.style.display = isDev ? "block" : "none";
        if (devGraphContainer) devGraphContainer.style.display = isDev ? "block" : "none";
        if (isDev) renderGraph();
    }

    if (devModeToggle) {
        devModeToggle.addEventListener("change", updateModeVisibility);
    }

    // Graph Tabs
    document.querySelectorAll(".graph-type-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            activeGraphType = e.target.getAttribute("data-graph") || "flog";
            renderGraph();
        });
    });

    // Render Vis.js Graph
    function renderGraph() {
        if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex] || !interactiveCanvas) return;
        const fnData = currentAnalysisData.functions[activeFnIndex];
        const rawNodes = (fnData.nodes && fnData.nodes[activeGraphType]) || [];
        const rawEdges = (fnData.edges && fnData.edges[activeGraphType]) || [];

        const nodes = rawNodes.map(n => ({
            id: n.id,
            label: n.label || n.var_name || n.name || n.kind || n.node_type || n.id,
            shape: "box",
        }));

        const edges = rawEdges.map(e => ({
            from: e.source,
            to: e.target,
            label: e.label || e.edge_type || "",
            arrows: "to",
        }));

        const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        const options = {
            physics: {
                solver: "forceAtlas2Based",
                stabilization: { iterations: 80 }
            }
        };

        if (networkInstance) networkInstance.destroy();
        networkInstance = new vis.Network(interactiveCanvas, data, options);

        // Outliers
        if (outliersContentList) {
            outliersContentList.innerHTML = "";
            const outliers = (fnData.graph_outliers && fnData.graph_outliers[activeGraphType]) || [];
            if (outliers.length === 0) {
                outliersContentList.innerHTML = "<p>No topological anomalies detected.</p>";
            } else {
                outliers.forEach(o => {
                    const div = document.createElement("div");
                    div.innerHTML = `<strong>[${o.severity}] ${o.title}</strong> (${o.cwe_id || ''})<p>${o.description}</p>`;
                    outliersContentList.appendChild(div);
                });
            }
        }
    }

    // Copy Patch
    if (copyPatchBtn && xaiPatchCode) {
        copyPatchBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(xaiPatchCode.textContent).then(() => {
                alert("Patch copied to clipboard!");
            });
        });
    }

    // Apply Patch
    if (applyPatchBtn && xaiPatchCode) {
        applyPatchBtn.addEventListener("click", async () => {
            const textToApply = xaiPatchCode.textContent;
            if (!textToApply || textToApply.startsWith("// No")) {
                alert("No patch to apply.");
                return;
            }
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
            const activeFn = currentAnalysisData.functions[activeFnIndex];

            try {
                const res = await fetch("/api/revisions/commit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        function_name: activeFn.name,
                        source_code: textToApply,
                        change_type: "PATCH_APPLIED",
                        patch_summary: "Applied Idiomatic Rust Refactoring Patch",
                    }),
                });
                const data = await res.json();
                if (data.success) {
                    if (codeEditor) codeEditor.value = textToApply;
                    alert("Patch applied! Re-analyzing...");
                    if (analyzeBtn) analyzeBtn.click();
                }
            } catch (err) {
                alert("Failed to commit revision: " + err.message);
            }
        });
    }

    // Revisions Drawer Toggle
    if (revisionsToggleBtn) {
        revisionsToggleBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) {
                alert("Please analyze code first.");
                return;
            }
            const fnName = currentAnalysisData.functions[activeFnIndex].name;
            if (drawerFnSubtitle) drawerFnSubtitle.textContent = `Subroutine: fn ${fnName}()`;

            try {
                const res = await fetch(`/api/revisions?function=${encodeURIComponent(fnName)}`);
                const data = await res.json();
                if (data.success && revisionsTimelineContainer) {
                    revisionsTimelineContainer.innerHTML = "";
                    const revs = data.revisions || [];
                    if (revs.length === 0 && revisionsEmptyState) {
                        revisionsEmptyState.style.display = "block";
                    } else {
                        if (revisionsEmptyState) revisionsEmptyState.style.display = "none";
                        revs.forEach(r => {
                            const card = document.createElement("div");
                            card.style.border = "1px solid #ccc";
                            card.style.padding = "8px";
                            card.style.margin = "8px 0";
                            card.innerHTML = `
                                <p><strong>Rev #${r.revision_number}</strong> (${r.change_type}) - RQI: ${r.rqi_score.toFixed(1)} [${r.grade}]</p>
                                <p><small>${r.timestamp_display}</small></p>
                                <p>${r.patch_summary}</p>
                                <button type="button" class="rb-btn" data-id="${r.revision_id}">Rollback to this</button>
                            `;
                            card.querySelector(".rb-btn").addEventListener("click", async () => {
                                const rbRes = await fetch("/api/revisions/rollback", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ revision_id: r.revision_id }),
                                });
                                const rbData = await rbRes.json();
                                if (rbData.success) {
                                    if (codeEditor) codeEditor.value = rbData.source_code;
                                    if (revisionHistoryDrawer) revisionHistoryDrawer.style.display = "none";
                                    alert("Rolled back! Re-analyzing...");
                                    if (analyzeBtn) analyzeBtn.click();
                                }
                            });
                            revisionsTimelineContainer.appendChild(card);
                        });
                    }
                }
            } catch (e) {
                alert("Failed to load revisions: " + e.message);
            }

            if (revisionHistoryDrawer) revisionHistoryDrawer.style.display = "block";
        });
    }

    if (closeDrawerBtn && revisionHistoryDrawer) {
        closeDrawerBtn.addEventListener("click", () => {
            revisionHistoryDrawer.style.display = "none";
        });
    }

    if (clearRevisionsBtn) {
        clearRevisionsBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) return;
            const fnName = currentAnalysisData.functions[activeFnIndex].name;
            await fetch(`/api/revisions?function=${encodeURIComponent(fnName)}`, { method: "DELETE" });
            alert("Revisions cleared.");
            if (revisionHistoryDrawer) revisionHistoryDrawer.style.display = "none";
            if (revCountBadge) revCountBadge.textContent = "0";
        });
    }

    // Export PDF
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener("click", async () => {
            if (!currentAnalysisData || !currentAnalysisData.functions[activeFnIndex]) {
                alert("No audit data available to export.");
                return;
            }
            try {
                const res = await fetch("/api/export/pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        function_data: currentAnalysisData.functions[activeFnIndex],
                        filename: "subroutine_audit.rs",
                    }),
                });
                if (!res.ok) throw new Error("Export failed with status " + res.status);
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `rustaudit_report_${currentAnalysisData.functions[activeFnIndex].name}.pdf`;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }, 200);
            } catch (err) {
                alert("PDF export failed: " + err.message);
            }
        });
    }
});

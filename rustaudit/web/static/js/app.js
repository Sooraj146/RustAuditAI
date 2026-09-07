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

    const astNodesCnt = document.getElementById("ast-nodes-cnt");
    const cfgCcCnt = document.getElementById("cfg-cc-cnt");
    const flogAllocCnt = document.getElementById("flog_alloc_cnt");
    const flogClonesCnt = document.getElementById("flog_clones_cnt");

    const xaiSection = document.getElementById("xai-section");
    const xaiExplanationText = document.getElementById("xai-explanation-text");
    const xaiPatchCode = document.getElementById("xai-patch-code");
    const copyPatchBtn = document.getElementById("copy-patch-btn");


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
                const prosList = vc.score === 100 ? vc.defaultPros : vc.defaultPros.slice(0, 1);

                let rationaleHtml = `<div class="rationale-group">`;
                prosList.forEach(p => {
                    rationaleHtml += `<span class="rationale-tag tag-pro"><i class="fa-solid fa-circle-check"></i> ${p}</span>`;
                });
                consList.forEach(c => {
                    rationaleHtml += `<span class="rationale-tag tag-con"><i class="fa-solid fa-circle-minus"></i> ${c}</span>`;
                });
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

        // Quality Deductions
        deductionsList.innerHTML = "";
        const allDeductions = Object.values(rqi.deductions).flat();
        if (allDeductions.length === 0) {
            const li = document.createElement("li");
            li.textContent = "No quality deductions detected. Subroutine is idiomatic and clean!";
            li.style.color = "#34d399";
            deductionsList.appendChild(li);
        } else {
            allDeductions.forEach(d => {
                const li = document.createElement("li");
                li.textContent = d;
                deductionsList.appendChild(li);
            });
        }

        // CPG Metrics
        astNodesCnt.textContent = fnData.cpg_summary.ast_nodes;
        cfgCcCnt.textContent = fnData.cpg_summary.cyclomatic_complexity;
        flogAllocCnt.textContent = fnData.cpg_summary.allocations;
        flogClonesCnt.textContent = fnData.cpg_summary.clones;

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
                    xaiExplanationText.textContent = fnData.xai_report.explanation || "No explanation output";
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

            if (n.node_type === "FunctionDecl" || n.node_type === "ENTRY" || n.node_type === "FnScope") color = "#06b6d4";
            if (n.node_type === "DecisionBlock" || n.is_decision) color = "#f59e0b";
            if (n.node_type === "HeapAllocation" || n.is_heap_alloc) color = "#a855f7";
            if (n.node_type === "ClonedBinding" || n.is_clone) color = "#ef4444";
            if (n.node_type === "UnsafeOperation" || n.is_unsafe) color = "#dc2626";

            return {
                id: n.id,
                label: label,
                color: { background: color, border: "#ffffff", highlight: { background: "#ffffff", border: color } },
                font: { color: "#ffffff", face: "Fira Code" },
                shape: "box",
                margin: 10,
            };
        });

        // Build Vis-Network Edges
        const edges = rawEdges.map(e => ({
            from: e.source,
            to: e.target,
            label: e.label || e.edge_type || "",
            font: { color: "#94a3b8", size: 10 },
            arrows: "to",
            color: { color: "#334155" },
        }));

        const container = interactiveCanvas;
        const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        const options = {
            physics: { solver: "forceAtlas2Based", stabilization: { iterations: 100 } },
            interaction: { hover: true, zoomView: true, dragView: true },
        };

        if (networkInstance) networkInstance.destroy();
        networkInstance = new vis.Network(container, data, options);

        // Render Graph Outliers for active graph type
        renderOutliers(fnData.graph_outliers[activeGraphType] || []);
    }

    function renderOutliers(outliersList) {
        outliersContentList.innerHTML = "";
        if (!outliersList || outliersList.length === 0) {
            outliersContentList.innerHTML = `<p style="font-size:0.8rem; color:#34d399;">No anomalies or topological outliers detected in ${activeGraphType.toUpperCase()} graph model.</p>`;
            return;
        }

        outliersList.forEach(item => {
            const card = document.createElement("div");
            card.className = `outlier-card-item severity-${item.severity}`;
            card.innerHTML = `
                <h5><span>${item.title}</span><span class="severity-badge">[${item.severity}]</span></h5>
                <p>${item.description}</p>
            `;
            outliersContentList.appendChild(card);
        });
    }
});


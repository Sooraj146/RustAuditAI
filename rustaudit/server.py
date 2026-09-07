"""
FastAPI Server for RustAuditAI Web Dashboard.
Provides REST API endpoints for code parsing, graph construction, RQI scoring, and XAI refactoring.
"""

from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder, GraphOutlierAnalyzer
from rustaudit.metrics import RQISynthesizer
from rustaudit.ai import XAIEngine

app = FastAPI(
    title="RustAuditAI API",
    description="Intra-Procedural Semantic Analysis & Software Quality Intelligence Framework",
    version="1.0.0",
)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "web" / "static"
TEMPLATES_DIR = BASE_DIR / "web" / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

parser = RustParser()
builder = CPGBuilder()
outlier_analyzer = GraphOutlierAnalyzer()
synthesizer = RQISynthesizer()
ai_engine = XAIEngine()


class AnalyzeRequest(BaseModel):
    code: str
    explain: bool = False


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    html_file = TEMPLATES_DIR / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI template not found")
    return html_file.read_text(encoding="utf-8")


@app.post("/api/analyze")
async def analyze_code(req: AnalyzeRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Empty Rust code payload")

    parse_res = parser.parse_code(req.code)

    if not parse_res.success:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": parse_res.error or "Syntax parse error"},
        )

    functions_data = []

    for fn in parse_res.functions:
        cpg = builder.build_cpg(fn)
        cpg_summary = cpg.summary()
        rqi_summary = synthesizer.compute_rqi(fn, cpg)
        outliers_report = outlier_analyzer.analyze_outliers(fn, cpg)

        fn_data = {
            "name": fn.name,
            "visibility": fn.visibility,
            "is_unsafe": fn.is_unsafe,
            "is_async": fn.is_async,
            "line_start": fn.line_start,
            "line_end": fn.line_end,
            "metrics": {
                "clone_count": fn.clone_count,
                "allocation_count": fn.allocation_count,
                "unsafe_block_count": fn.unsafe_block_count,
                "borrow_count": fn.borrow_count,
                "loop_count": fn.loop_count,
                "branch_count": fn.branch_count,
            },
            "cpg_summary": cpg_summary,
            "rqi": rqi_summary.to_dict(),
            "graph_outliers": outliers_report.to_dict(),
            "nodes": {
                "ast": [{"id": n, **d} for n, d in cpg.ast.nodes(data=True)],
                "cfg": [{"id": n, **d} for n, d in cpg.cfg.nodes(data=True)],
                "flog": [{"id": n, **d} for n, d in cpg.flog.nodes(data=True)],
            },
            "edges": {
                "ast": [{"source": u, "target": v, **d} for u, v, d in cpg.ast.edges(data=True)],
                "cfg": [{"source": u, "target": v, **d} for u, v, d in cpg.cfg.edges(data=True)],
                "flog": [{"source": u, "target": v, **d} for u, v, d in cpg.flog.edges(data=True)],
            },
        }

        if req.explain:
            try:
                lines = req.code.splitlines()
                if fn.line_start > 0 and fn.line_end <= len(lines):
                    fn_code = "\n".join(lines[fn.line_start - 1 : fn.line_end])
                else:
                    fn_code = req.code

                report = ai_engine.generate_explanation(fn, cpg, rqi_summary, fn_code)
                fn_data["xai_report"] = {
                    "explanation": report.explanation,
                    "refactored_code": report.refactored_code,
                    "diff_text": report.diff_text,
                    "metrics_summary": report.metrics_summary,
                }
            except Exception as e:
                fn_data["xai_report"] = {"error": f"Failed to generate AI report: {str(e)}"}

        functions_data.append(fn_data)

    return {
        "success": True,
        "function_count": len(functions_data),
        "functions": functions_data,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rustaudit.server:app", host="127.0.0.1", port=8000, reload=True)

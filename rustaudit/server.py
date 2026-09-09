"""
FastAPI Server for RustAuditAI Web Dashboard.
Provides REST API endpoints for code parsing, graph construction, RQI scoring, and XAI refactoring.
"""

from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, ConfigDict

from rustaudit.parser import RustParser
from rustaudit.graph import CPGBuilder, GraphOutlierAnalyzer
from rustaudit.metrics import RQISynthesizer
from rustaudit.ai import XAIEngine
from rustaudit.reports import RustAuditPDFReportGenerator, generate_pdf_report

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


class ExportReportRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    audit_data: Optional[dict] = None
    function_data: Optional[dict] = None
    filename: Optional[str] = "rust_subroutine.rs"
    function_index: Optional[int] = None


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    html_file = TEMPLATES_DIR / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI template not found")
    return html_file.read_text(encoding="utf-8")


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handle .rs source file uploads. Validates extension, extracts text,
    and returns code content to populate the web UI editor.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename.endswith(".rs"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: '{file.filename}'. RustAuditAI requires a Rust source file (.rs).",
        )

    try:
        content_bytes = await file.read()
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File encoding error. Please ensure the uploaded file is valid UTF-8 text.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read uploaded file: {str(e)}",
        )

    return {
        "success": True,
        "filename": file.filename,
        "code": content,
        "size": len(content_bytes),
    }


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
            "cwe_tags": rqi_summary.get_cwe_tags(),
            "cwe_summary": rqi_summary.get_cwe_summary(),
            "graph_outliers": outliers_report.to_dict(),
            "nodes": {
                "ast": [{"id": n, **d} for n, d in cpg.ast.nodes(data=True)],
                "cfg": [{"id": n, **d} for n, d in cpg.cfg.nodes(data=True)],
                "flog": [{"id": n, **d} for n, d in cpg.flog.nodes(data=True)],
                "cpg": [{"id": n, **d} for n, d in cpg.unified_cpg.nodes(data=True)],
            },
            "edges": {
                "ast": [{"source": u, "target": v, **d} for u, v, d in cpg.ast.edges(data=True)],
                "cfg": [{"source": u, "target": v, **d} for u, v, d in cpg.cfg.edges(data=True)],
                "flog": [{"source": u, "target": v, **d} for u, v, d in cpg.flog.edges(data=True)],
                "cpg": [{"source": u, "target": v, **d} for u, v, d in cpg.unified_cpg.edges(data=True)],
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

    total_cwe_count = sum(len(f["cwe_tags"]) for f in functions_data)
    total_cwe_critical = sum(f["cwe_summary"]["critical"] for f in functions_data)
    total_cwe_high = sum(f["cwe_summary"]["high"] for f in functions_data)
    total_cwe_medium = sum(f["cwe_summary"]["medium"] for f in functions_data)
    total_cwe_low = sum(f["cwe_summary"]["low"] for f in functions_data)

    return {
        "success": True,
        "function_count": len(functions_data),
        "functions": functions_data,
        "overall_cwe_summary": {
            "total": total_cwe_count,
            "critical": total_cwe_critical,
            "high": total_cwe_high,
            "medium": total_cwe_medium,
            "low": total_cwe_low,
        },
    }


@app.post("/api/export/pdf")
async def export_pdf_report(req: ExportReportRequest):
    data = req.function_data or req.audit_data
    if data is None:
        raw_dict = req.model_dump()
        if "rqi" in raw_dict or "functions" in raw_dict or "name" in raw_dict:
            data = raw_dict
        else:
            raise HTTPException(status_code=400, detail="Missing audit data for PDF report export")

    if req.function_index is not None and isinstance(data, dict) and "functions" in data and isinstance(data["functions"], list):
        if 0 <= req.function_index < len(data["functions"]):
            data = data["functions"][req.function_index]

    try:
        pdf_bytes = generate_pdf_report(data, filename=req.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")

    fn_name = "subroutine"
    if isinstance(data, dict):
        fn_name = data.get("name", "subroutine")
    clean_fn_name = "".join(c for c in str(fn_name) if c.isalnum() or c in ("-", "_")) or "subroutine"
    download_filename = f"rustaudit_report_{clean_fn_name}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{download_filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rustaudit.server:app", host="127.0.0.1", port=8000, reload=True)

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
from rustaudit.revision import get_revision_manager, CodeRevision

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

@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static/") or request.url.path == "/":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

parser = RustParser()
builder = CPGBuilder()
outlier_analyzer = GraphOutlierAnalyzer()
synthesizer = RQISynthesizer()
ai_engine = XAIEngine()
revision_mgr = get_revision_manager()


class AnalyzeRequest(BaseModel):
    code: str
    explain: bool = False


class CommitRevisionRequest(BaseModel):
    function_name: str
    source_code: str
    rqi_score: Optional[float] = None
    grade: Optional[str] = None
    vector_scores: Optional[dict] = None
    change_type: Optional[str] = "PATCH_APPLIED"
    patch_summary: Optional[str] = "Applied Idiomatic Rust Refactoring Patch"


class RollbackRequest(BaseModel):
    revision_id: str


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

        # Automatic baseline revision recording (SRS §4.6.7)
        existing_revs = revision_mgr.get_revisions(fn.name)
        if not existing_revs:
            revision_mgr.record_revision(
                function_name=fn.name,
                source_code=req.code,
                rqi_score=rqi_summary.rqi_score,
                grade=rqi_summary.grade,
                vector_scores={
                    "safety": rqi_summary.vectors.safety,
                    "performance": rqi_summary.vectors.performance,
                    "maintainability": rqi_summary.vectors.maintainability,
                    "security": rqi_summary.vectors.security,
                },
                change_type="INITIAL",
                patch_summary=f"Initial Subroutine Audit (RQI {rqi_summary.rqi_score:.1f})",
            )
            existing_revs = revision_mgr.get_revisions(fn.name)

        fn_data["revisions"] = [r.to_dict() for r in existing_revs]
        fn_data["total_revisions"] = len(existing_revs)

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

    fn_name = "complete_audit"
    if isinstance(data, dict) and data.get("name"):
        fn_name = data["name"]
    elif req.filename:
        from pathlib import Path
        fn_name = Path(req.filename).stem
    elif isinstance(data, dict) and data.get("filename"):
        from pathlib import Path
        fn_name = Path(data["filename"]).stem

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


@app.get("/api/revisions")
async def get_revisions(function: Optional[str] = None):
    """
    Returns the intra-procedural revision ledger for the specified subroutine (SRS §4.6.7).
    """
    revs = revision_mgr.get_revisions(function)
    return {
        "success": True,
        "function_name": function,
        "total_revisions": len(revs),
        "revisions": [r.to_dict() for r in revs],
    }


@app.post("/api/revisions/commit")
async def commit_revision(req: CommitRevisionRequest):
    """
    Records an approved modification layer in the intra-procedural revision database (SRS §4.6.6 & §4.6.7).
    """
    rqi_score = req.rqi_score
    grade = req.grade or "Grade A"
    vector_scores = req.vector_scores or {"safety": 100.0, "performance": 100.0, "maintainability": 100.0, "security": 100.0}

    # If metrics were not passed, calculate them deterministically
    if rqi_score is None:
        try:
            parsed = parser.parse_code(req.source_code)
            if parsed.success and parsed.functions:
                target_fn = next((f for f in parsed.functions if f.name == req.function_name), parsed.functions[0])
                cpg = builder.build_cpg(target_fn)
                rqi_res = synthesizer.compute_rqi(target_fn, cpg)
                rqi_score = rqi_res.rqi_score
                grade = rqi_res.grade
                vector_scores = {
                    "safety": rqi_res.vectors.safety,
                    "performance": rqi_res.vectors.performance,
                    "maintainability": rqi_res.vectors.maintainability,
                    "security": rqi_res.vectors.security,
                }
            else:
                rqi_score = 100.0
        except Exception:
            rqi_score = 100.0

    rev = revision_mgr.record_revision(
        function_name=req.function_name,
        source_code=req.source_code,
        rqi_score=rqi_score,
        grade=grade,
        vector_scores=vector_scores,
        change_type=req.change_type or "PATCH_APPLIED",
        patch_summary=req.patch_summary or "Approved Refactoring Patch",
    )

    all_revs = revision_mgr.get_revisions(req.function_name)
    return {
        "success": True,
        "revision": rev.to_dict(),
        "total_revisions": len(all_revs),
        "revisions": [r.to_dict() for r in all_revs],
    }


@app.post("/api/revisions/rollback")
async def rollback_revision(req: RollbackRequest):
    """
    Restores the subroutine back to any earlier revision state and logs the rollback (SRS §4.6.7).
    """
    restored = revision_mgr.rollback_to_revision(req.revision_id)
    if not restored:
        raise HTTPException(status_code=404, detail=f"Revision ID '{req.revision_id}' not found")

    all_revs = revision_mgr.get_revisions(restored.function_name)
    return {
        "success": True,
        "restored_revision": restored.to_dict(),
        "source_code": restored.source_code,
        "total_revisions": len(all_revs),
        "revisions": [r.to_dict() for r in all_revs],
    }


@app.delete("/api/revisions")
async def clear_revisions(function: Optional[str] = None):
    """
    Clears the revision history for a function or all functions.
    """
    revision_mgr.clear_revisions(function)
    return {"success": True, "cleared_function": function}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rustaudit.server:app", host="127.0.0.1", port=8000, reload=True)

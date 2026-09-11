"""
Unit and Integration tests for Intra-Procedural Code Revision & Rollback (SRS §4.6.7).
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.revision import RevisionManager, get_revision_manager
from rustaudit.server import app


def test_revision_manager_lifecycle():
    """Validates full lifecycle of RevisionManager: record, history, rollback, clear."""
    mgr = RevisionManager(db_path=":memory:")

    # 1. Record Initial Revision
    r1 = mgr.record_revision(
        function_name="calc_sum",
        source_code="pub fn calc_sum(x: i32) -> i32 { x + 1 }",
        rqi_score=75.0,
        grade="Grade B",
        vector_scores={"safety": 80.0, "performance": 70.0, "maintainability": 75.0, "security": 80.0},
        change_type="INITIAL",
        patch_summary="Initial subroutine audit",
    )
    assert r1.revision_number == 1
    assert r1.rqi_score == 75.0
    assert r1.change_type == "INITIAL"
    assert r1.is_active is True

    # 2. Record Approved Patch
    r2 = mgr.record_revision(
        function_name="calc_sum",
        source_code="pub fn calc_sum(x: i32) -> i32 { x.saturating_add(1) }",
        rqi_score=100.0,
        grade="Grade A+",
        vector_scores={"safety": 100.0, "performance": 100.0, "maintainability": 100.0, "security": 100.0},
        change_type="PATCH_APPLIED",
        patch_summary="Applied saturating add patch",
    )
    assert r2.revision_number == 2
    assert r2.rqi_score == 100.0
    assert r2.change_type == "PATCH_APPLIED"

    # Verify r1 is now inactive and r2 is active
    r1_updated = mgr.get_revision(r1.revision_id)
    assert r1_updated.is_active is False
    r2_updated = mgr.get_revision(r2.revision_id)
    assert r2_updated.is_active is True

    # 3. Retrieve Chronological History
    history = mgr.get_revisions("calc_sum")
    assert len(history) == 2
    assert history[0].revision_number == 1
    assert history[1].revision_number == 2

    # 4. Rollback to Revision 1
    rolled = mgr.rollback_to_revision(r1.revision_id)
    assert rolled is not None
    assert rolled.revision_number == 3
    assert rolled.change_type == "ROLLBACK"
    assert rolled.source_code == r1.source_code
    assert rolled.rqi_score == r1.rqi_score
    assert rolled.is_active is True

    # Check total revisions is now 3
    history3 = mgr.get_revisions("calc_sum")
    assert len(history3) == 3

    # 5. Clear Revisions
    mgr.clear_revisions("calc_sum")
    assert len(mgr.get_revisions("calc_sum")) == 0


def test_server_revisions_api():
    """Validates FastAPI REST endpoints for revision management."""
    client = TestClient(app)

    # 1. Clear any prior revisions
    client.delete("/api/revisions?function=test_api_subroutine")

    # 2. Commit a new revision
    commit_payload = {
        "function_name": "test_api_subroutine",
        "source_code": "pub fn test_api_subroutine() -> i32 { 42 }",
        "rqi_score": 100.0,
        "grade": "A+ (Idiomatic)",
        "vector_scores": {"safety": 100.0, "performance": 100.0, "maintainability": 100.0, "security": 100.0},
        "change_type": "INITIAL",
        "patch_summary": "Initial baseline",
    }
    res = client.post("/api/revisions/commit", json=commit_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    rev = data["revision"]
    assert rev["function_name"] == "test_api_subroutine"
    assert rev["revision_number"] == 1
    rev_id = rev["revision_id"]

    # 3. Fetch revisions list
    get_res = client.get("/api/revisions?function=test_api_subroutine")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["total_revisions"] == 1
    assert get_data["revisions"][0]["revision_id"] == rev_id

    # 4. Rollback via API
    rollback_res = client.post("/api/revisions/rollback", json={"revision_id": rev_id})
    assert rollback_res.status_code == 200
    rollback_data = rollback_res.json()
    assert rollback_data["success"] is True
    assert rollback_data["restored_revision"]["revision_number"] == 2
    assert rollback_data["restored_revision"]["change_type"] == "ROLLBACK"
    assert rollback_data["source_code"] == commit_payload["source_code"]

    # Clean up
    client.delete("/api/revisions?function=test_api_subroutine")


def test_automatic_baseline_in_analyze():
    """Validates that /api/analyze automatically creates a baseline revision for subroutines."""
    client = TestClient(app)
    fn_name = "auto_rev_check"
    client.delete(f"/api/revisions?function={fn_name}")

    code = f"pub fn {fn_name}() -> bool {{ true }}"
    res = client.post("/api/analyze", json={"code": code, "explain": False})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["functions"]) == 1

    fn_res = data["functions"][0]
    assert "revisions" in fn_res
    assert fn_res["total_revisions"] >= 1
    assert fn_res["revisions"][0]["function_name"] == fn_name
    assert fn_res["revisions"][0]["change_type"] == "INITIAL"

    # Clean up
    client.delete(f"/api/revisions?function={fn_name}")

import io
import json
import urllib.request
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_full_pipeline():
    print("==================================================")
    print(" RustAuditAI Graph & File Upload Verification")
    print("==================================================")

    # 1. Verify UI Template and Assets
    req = urllib.request.Request(f"{BASE_URL}/")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        html = resp.read().decode("utf-8")

    assert 'id="upload-file-btn"' in html, "Upload button missing"
    assert 'id="file-upload-input"' in html, "File upload input missing"
    assert 'id="file-badge"' in html, "File badge missing"
    assert 'id="drop-overlay"' in html, "Drop overlay missing"
    assert 'data-graph="cpg"' in html, "Unified CPG tab missing"
    assert 'id="cpg-edges-cnt"' in html, "CPG edges metric missing"
    print("[PASS] Web UI Template contains all file upload and Unified CPG components.")

    # 2. Verify /api/upload with real .rs file
    sample_rs_path = Path("tests/samples/sample_func.rs")
    sample_content = sample_rs_path.read_text(encoding="utf-8")

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="sample_func.rs"\r\n'
        f"Content-Type: text/plain\r\n\r\n"
        f"{sample_content}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    upload_req = urllib.request.Request(
        f"{BASE_URL}/api/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(upload_req) as resp:
        assert resp.status == 200
        upload_data = json.loads(resp.read().decode("utf-8"))

    assert upload_data["success"] is True
    assert upload_data["filename"] == "sample_func.rs"
    uploaded_code = upload_data["code"]
    print(f"[PASS] File Upload API succeeded: {upload_data['filename']} ({upload_data['size']} bytes).")

    # 3. Simulate User Editing Code in Web UI
    edited_code = uploaded_code + """\n
// User Edited Subroutine: Adding custom function to test in-browser editing
pub fn custom_user_routine(items: Vec<String>) -> usize {
    let mut count = 0;
    for item in items {
        if item.len() > 5 {
            count += 1;
        }
    }
    count
}
"""
    print("[INFO] Simulated user editing code in textarea (appended custom_user_routine).")

    # 4. Execute Graph Audit on Edited Code
    analyze_payload = json.dumps({"code": edited_code, "explain": False}).encode("utf-8")
    analyze_req = urllib.request.Request(
        f"{BASE_URL}/api/analyze",
        data=analyze_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(analyze_req) as resp:
        assert resp.status == 200
        audit_data = json.loads(resp.read().decode("utf-8"))

    assert audit_data["success"] is True
    assert audit_data["function_count"] == 3
    print(f"[PASS] Graph Audit executed successfully: {audit_data['function_count']} functions analyzed.")

    for fn in audit_data["functions"]:
        print(f"\n--- Function: fn {fn['name']}() ---")
        cpg_sum = fn["cpg_summary"]
        print(f"  AST Nodes: {cpg_sum['ast_nodes']}, Edges: {cpg_sum['ast_edges']}")
        print(f"  CFG Nodes: {cpg_sum['cfg_nodes']}, Edges: {cpg_sum['cfg_edges']} (Complexity: {cpg_sum['cyclomatic_complexity']})")
        print(f"  FLOG Nodes: {cpg_sum['flog_nodes']}, Edges: {cpg_sum['flog_edges']} (Clones: {cpg_sum['clones']}, Alloc: {cpg_sum['allocations']})")
        print(f"  Unified CPG Nodes: {cpg_sum['cpg_nodes']}, Edges: {cpg_sum['cpg_edges']}")
        print(f"  RQI Score: {fn['rqi']['rqi_score']} ({fn['rqi']['grade']})")

        # Verify CPG nodes and edges are present in payload
        assert "cpg" in fn["nodes"]
        assert "cpg" in fn["edges"]
        assert len(fn["nodes"]["cpg"]) == cpg_sum["cpg_nodes"]
        assert len(fn["edges"]["cpg"]) == cpg_sum["cpg_edges"]

        # Verify cross-layer edges exist
        cross_edges = [e for e in fn["edges"]["cpg"] if "AST_TO_CFG" in e.get("edge_type", "") or "AST_TO_FLOG" in e.get("edge_type", "") or "CFG_TO_FLOG" in e.get("edge_type", "")]
        print(f"  Cross-layer Semantic Edges in Unified CPG: {len(cross_edges)}")
        assert len(cross_edges) > 0, "No cross-layer edges found in CPG"

    print("\n==================================================")
    print(" ALL GRAPH PIPELINE & FILE UPLOAD TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    test_full_pipeline()

import io
from pathlib import Path
from fastapi.testclient import TestClient
from rustaudit.server import app

client = TestClient(app)

def test_upload_valid_rs_file():
    sample_code = """pub fn hello_world() -> i32 {
    let x = 42;
    x
}"""
    file_bytes = sample_code.encode("utf-8")
    response = client.post(
        "/api/upload",
        files={"file": ("hello.rs", io.BytesIO(file_bytes), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "hello.rs"
    assert "pub fn hello_world" in data["code"]

def test_upload_invalid_extension():
    response = client.post(
        "/api/upload",
        files={"file": ("malicious.py", io.BytesIO(b"print('hello')"), "text/plain")},
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_analyze_includes_cpg():
    sample_code = """pub fn process(data: &str) -> String {
    let mut result = String::from(data);
    let dup = result.clone();
    dup
}"""
    response = client.post(
        "/api/analyze",
        json={"code": sample_code, "explain": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["functions"]) == 1
    fn = data["functions"][0]
    assert "cpg" in fn["nodes"]
    assert "cpg" in fn["edges"]
    assert len(fn["nodes"]["cpg"]) > 0
    assert len(fn["edges"]["cpg"]) > 0

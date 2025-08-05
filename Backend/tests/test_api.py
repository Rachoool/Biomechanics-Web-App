import os
import sys
import pytest

# Ensure Backend directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.app import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    app.config['UPLOAD_FOLDER'] = tmp_path
    monkeypatch.setattr("Backend.app.UPLOAD_FOLDER", tmp_path)
    with app.test_client() as client:
        yield client

def test_hello(client):
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Hello from Flask!"

def test_upload_and_list_models(client, tmp_path):
    test_file = tmp_path / "test.stl"
    test_file.write_text("dummy stl content")
    with open(test_file, "rb") as f:
        resp = client.post("/api/upload", data={"files": f})
    assert resp.status_code == 200

    resp = client.get("/api/models")
    assert resp.status_code == 200
    data = resp.get_json()["models"]
    assert "test.stl" in data

def test_upload_invalid_file(client, tmp_path):
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("invalid")
    with open(invalid_file, "rb") as f:
        resp = client.post("/api/upload", data={"files": f})
    assert resp.status_code == 400

def test_delete_file(client, tmp_path):
    test_file = tmp_path / "test.stl"
    test_file.write_text("dummy stl content")
    with open(test_file, "rb") as f:
        client.post("/api/upload", data={"files": f})

    resp = client.delete("/api/delete/test.stl")
    assert resp.status_code == 200

def test_delete_nonexistent_file(client):
    resp = client.delete("/api/delete/not_exist.stl")
    assert resp.status_code == 404

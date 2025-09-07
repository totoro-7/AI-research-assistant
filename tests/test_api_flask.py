import json
import pytest
from app.server_flask import create_app

@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert "torch_version" in data

def test_generate_gap(client):
    r = client.post("/generate_gap", json={"topic": "AI in healthcare"})
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data["research_gaps"], str) and len(data["research_gaps"].strip()) > 0

def test_generate_manuscript(client):
    r = client.post("/generate_manuscript", json={"gap": "Lack of randomized trials"})
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data["manuscript"], str) and len(data["manuscript"].strip()) > 0

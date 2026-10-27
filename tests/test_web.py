from unittest import mock
import pytest
from fastapi.testclient import TestClient
from app.web.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "GitNecromancer" in response.text
    assert "The Git Catacombs" in response.text


def test_ofrenda_page(client):
    response = client.get("/ofrenda")
    assert response.status_code == 200
    assert "Ofrenda" in response.text


def test_api_graveyard(client):
    response = client.get("/api/graveyard?demo=true")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_api_seance_invocation(client):
    response = client.post("/api/seance/branch-feat-graphql-migration?demo=true")
    assert response.status_code == 200
    data = response.json()
    assert "ghost_monologue" in data
    assert "cause_of_death_analysis" in data
    assert "suggested_action" in data


@mock.patch("app.web.server.generate_resurrection_patch")
def test_api_resurrect(mock_patch, client):
    mock_patch.return_value = {
        "success": True,
        "patch": "diff --git a/test.py b/test.py\n+hello",
        "files_changed": 1,
        "instructions": "git apply resurrection.patch"
    }
    response = client.post("/api/resurrect/feat-graphql-migration")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "patch" in data


def test_api_exorcise(client, tmp_path):
    response = client.post("/api/exorcise", json={
        "target": "feat/abandoned-branch",
        "epitaph": "Rest in peace, old friend.",
        "delete_branch": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

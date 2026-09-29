from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "LegalEase"


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_generate_document():

    payload = {
        "document_type": "Non-Disclosure Agreement",
        "parties": (
            "Party 1: ABC Technologies\n"
            "Party 2: John Doe"
        ),
        "terms": (
            "Confidentiality: 2 years; "
            "Notice period: 30 days"
        ),
        "date": "01 October 2026"
    }

    response = client.post(
        "/api/generate",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["content"]) > 0
import json

from fastapi.testclient import TestClient

from app import summarizer
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"ok": True}


def test_summarize_endpoint(monkeypatch):
    reply = json.dumps({"summary": "Invoice shows the wrong VAT.", "priority": "low", "category": "billing"})
    monkeypatch.setattr(summarizer.llm, "complete", lambda system, user: reply)
    res = client.post("/tickets/summarize", json={"subject": "VAT", "body": "My invoice VAT is wrong."})
    assert res.status_code == 200
    assert res.json()["category"] == "billing"


def test_similar_endpoint(monkeypatch):
    monkeypatch.setattr(summarizer.llm, "embed", lambda text: [1.0, 0.0] if "login" in text else [0.0, 1.0])
    res = client.post("/tickets/similar", json={"text": "login loop", "past": [{"id": "A", "text": "login fails"}, {"id": "B", "text": "refund"}]})
    assert res.json()["matches"][0]["id"] == "A"

import json

from app import summarizer


def test_summary_parses_model_json(monkeypatch):
    reply = json.dumps({"summary": "Customer cannot log in after reset.", "priority": "high", "category": "Auth"})
    monkeypatch.setattr(summarizer.llm, "complete", lambda system, user: reply)
    out = summarizer.summarize_ticket("Login broken", "I reset my password and now I am locked out.")
    assert out == {"summary": "Customer cannot log in after reset.", "priority": "high", "category": "auth"}


def test_unknown_priority_falls_back_to_medium(monkeypatch):
    monkeypatch.setattr(summarizer.llm, "complete", lambda system, user: json.dumps({"summary": "x", "priority": "urgent"}))
    assert summarizer.summarize_ticket("s", "b")["priority"] == "medium"


def test_non_json_reply_is_kept_as_summary(monkeypatch):
    monkeypatch.setattr(summarizer.llm, "complete", lambda system, user: "  Refund request for order 1182  ")
    out = summarizer.summarize_ticket("Refund", "Please refund order 1182.")
    assert out == {"summary": "Refund request for order 1182", "priority": "medium", "category": "other"}


def test_most_similar_ranks_by_cosine(monkeypatch):
    vectors = {"printer jams": [1.0, 0.0], "paper stuck": [0.9, 0.1], "billing": [0.0, 1.0]}
    monkeypatch.setattr(summarizer.llm, "embed", lambda text: vectors[text])
    past = [{"id": "T-1", "text": "billing"}, {"id": "T-2", "text": "paper stuck"}]
    assert [m["id"] for m in summarizer.most_similar("printer jams", past)] == ["T-2", "T-1"]

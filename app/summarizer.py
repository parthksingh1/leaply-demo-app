"""Summarise support tickets and find similar past tickets."""

import json
import math

from app import llm

SYSTEM_PROMPT = (
    "You triage customer support tickets. Reply with JSON only: "
    '{"summary": "<one sentence>", "priority": "low|medium|high", "category": "<one word>"}'
)

PRIORITIES = {"low", "medium", "high"}


def summarize_ticket(subject, body):
    """Ask the model for a one-line summary, a priority and a category."""
    raw = llm.complete(SYSTEM_PROMPT, f"Subject: {subject}\n\n{body}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"summary": raw.strip()[:200], "priority": "medium", "category": "other"}
    priority = data.get("priority", "medium")
    return {
        "summary": str(data.get("summary", "")).strip(),
        "priority": priority if priority in PRIORITIES else "medium",
        "category": str(data.get("category", "other")).lower(),
    }


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def most_similar(text, past_tickets, top=3):
    """Rank past tickets ({"id", "text"}) by similarity to text."""
    query = llm.embed(text)
    scored = [(cosine(query, llm.embed(t["text"])), t["id"]) for t in past_tickets]
    scored.sort(reverse=True)
    return [{"id": ticket_id, "score": round(score, 3)} for score, ticket_id in scored[:top]]

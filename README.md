# Support ticket summarizer

A small FastAPI service that summarises customer support tickets and finds similar past tickets, using the OpenAI API.

```
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload
```

- `POST /tickets/summarize` with `{"subject": "...", "body": "..."}` returns a one-line summary, a priority and a category.
- `POST /tickets/similar` with `{"text": "...", "past": [{"id": "...", "text": "..."}]}` ranks past tickets by similarity.

Tests mock the OpenAI calls, so they run without a key:

```
pytest -q
```

This repository is a demo target for [Leaply](https://github.com/parthksingh1/Leaply): it was written against the old OpenAI Python SDK (v0.28) on purpose, so Leaply can migrate it to v1 in a real pull request.

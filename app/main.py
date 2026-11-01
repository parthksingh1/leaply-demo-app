"""HTTP API: POST /tickets/summarize and POST /tickets/similar."""

from fastapi import FastAPI
from pydantic import BaseModel

from app.summarizer import most_similar, summarize_ticket

app = FastAPI(title="Support ticket summarizer")


class Ticket(BaseModel):
    subject: str
    body: str


class PastTicket(BaseModel):
    id: str
    text: str


class SimilarRequest(BaseModel):
    text: str
    past: list[PastTicket]


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/tickets/summarize")
def summarize(ticket: Ticket):
    return summarize_ticket(ticket.subject, ticket.body)


@app.post("/tickets/similar")
def similar(req: SimilarRequest):
    return {"matches": most_similar(req.text, [p.model_dump() for p in req.past])}

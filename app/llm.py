"""Thin wrapper around the OpenAI API so the rest of the app never imports it directly."""

import os
import time

import openai
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-3.5-turbo")
EMBEDDING_MODEL = "text-embedding-ada-002"


def complete(system, user, temperature=0.2):
    """Return the assistant's reply for one system + user message."""
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


def embed(text, retries=3):
    """Return the embedding vector for one piece of text, retrying on rate limits."""
    for attempt in range(retries):
        try:
            resp = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
            return resp.data[0].embedding
        except openai.RateLimitError:
            time.sleep(2**attempt)
    raise RuntimeError("embedding failed: rate limited")

"""
AI Study Notes Summarizer - Backend API
------------------------------------------
Run with: uvicorn main:app --reload

POST /summarize takes raw notes/text and returns:
- a concise summary
- a list of auto-generated flashcards (question/answer pairs)
"""

import os
import re
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI, AuthenticationError

app = FastAPI(title="AI Study Notes Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_MODEL = "gpt-4o-mini"


class SummarizeRequest(BaseModel):
    notes: str
    num_flashcards: int = 5
    api_key: Optional[str] = None


class Flashcard(BaseModel):
    question: str
    answer: str


class SummarizeResponse(BaseModel):
    summary: str
    flashcards: List[Flashcard]


def parse_response(text: str):
    # Expected format:
    # SUMMARY: ...
    # FLASHCARDS:
    # Q: ...
    # A: ...
    # Q: ...
    # A: ...
    summary_match = re.search(r"SUMMARY:\s*(.*?)(?=FLASHCARDS:|$)", text, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else text.strip()

    qa_pairs = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=Q:|$)", text, re.DOTALL)
    flashcards = [
        Flashcard(question=q.strip(), answer=a.strip())
        for q, a in qa_pairs
    ]

    return summary, flashcards


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    if not req.notes.strip():
        raise HTTPException(status_code=400, detail="Notes text is empty.")

    api_key = req.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="No API key provided. Pass one in the request or set OPENAI_API_KEY on the server.",
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""You are a study assistant. Read the notes below and produce:

1. A clear, concise summary (4-6 sentences) covering the key points.
2. Exactly {req.num_flashcards} flashcards testing the most important concepts.

NOTES:
{req.notes}

Respond in EXACTLY this format, nothing else:
SUMMARY: <summary text>
FLASHCARDS:
Q: <question 1>
A: <answer 1>
Q: <question 2>
A: <answer 2>
(continue for all {req.num_flashcards} flashcards)
"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=900,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid OpenAI API key.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI request failed: {str(e)}")

    text = response.choices[0].message.content
    summary, flashcards = parse_response(text)

    return SummarizeResponse(summary=summary, flashcards=flashcards)


@app.get("/health")
def health():
    return {"status": "ok"}


frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

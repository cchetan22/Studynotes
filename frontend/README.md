# AI Study Notes Summarizer — Web App

Paste any notes, textbook chapter, or article, and get:
- a concise summary
- auto-generated flashcards (click to reveal the answer)

Same structure as the resume matcher: FastAPI backend + a single HTML frontend,
one server, one port.

```
notes-summarizer/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

---

## Step 1 — Set up the folder

Download the files and arrange them exactly like this, with `backend` and
`frontend` as sibling folders:

```
notes-summarizer/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

## Step 2 — Open in VS Code

File → Open Folder → select `notes-summarizer`

## Step 3 — Open a terminal and go into backend

```bash
cd backend
```

## Step 4 — Create and activate a virtual environment

```bash
python -m venv venv
```

Activate it:
- Windows (PowerShell): `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

You should see `(venv)` appear at the start of your terminal line.

## Step 5 — Install dependencies

```bash
pip install -r requirements.txt
```

This is a small install — just FastAPI, Uvicorn, and the OpenAI SDK (no
embedding model this time, so it's much faster than the resume matcher).

## Step 6 — Start the server

```bash
uvicorn main:app --reload
```

Wait for:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal running.

## Step 7 — Open the app

Go to:

```
http://localhost:8000
```

## Step 8 — Use it

1. Paste your notes into the text box
2. Set how many flashcards you want (default 5)
3. Paste your OpenAI API key
4. Click **Summarize & generate flashcards**
5. Click any flashcard to flip it and reveal the answer

---

## Troubleshooting

Same fixes as the resume matcher project:
- "Invalid OpenAI API key" → check the key and that billing is set up on platform.openai.com
- "Network error" → make sure the `uvicorn` terminal is still running
- Port already in use → `uvicorn main:app --reload --port 8001`, then open `http://localhost:8001`

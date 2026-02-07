# CivicAI – Smart Grievance Platform

Production-oriented full-stack starter with FastAPI backend, React frontend, TF-IDF retrieval, and Level-1/Level-2 escalation flow.

## Folder Structure

- `backend/` FastAPI app, APIs, DB models, AI service, tests
- `frontend/` React + Tailwind + Framer Motion multi-page UI
- `ai/` training scripts
- `infra/` Docker compose
- `data/` datasets (`bbmp_reddit_data.csv` expected)
- `docs/` API docs

## Phase 1 (Architecture + Setup)
- Clean modular backend and frontend foundations.

## Phase 2 (Backend APIs)
Implemented:
- `POST /chat`
- `POST /complaint`
- `GET /status/{ticket_id}`
- `GET /history/{user_id}`
- `POST /feedback`
- `GET /analytics`

## Phase 3 (AI Engine)
- Hybrid TF-IDF matching for category/solution/department retrieval.
- Similar-case retrieval.
- Severity heuristic for escalation.

## Phase 4 (Frontend)
- Landing, Chat, History, Status, Admin, Analytics pages.
- Glassmorphism style, responsive layout, animated components.

## Local Run

### Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_demo_dataset.py   # only if dataset missing
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
cd infra
docker compose up --build
```

## Notes
- Place your `bbmp_reddit_data.csv` in `data/` with columns:
  `text, category, solution, department, location, resolved_status`.
- This is production-ready scaffolding with core functionality; add auth endpoints and CI/CD next for enterprise deployment.

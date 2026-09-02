# A.L.F.R.E.D.

**Autonomous Logistical Framework for Reliable Execution of Directives**

A.L.F.R.E.D. is an AI-powered personal assistant that translates natural-language goals into multi-step task plans, executes them using integrated tools, and verifies the results — all through a dark, retro-futuristic industrial interface.

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    FRONTEND (Vite + React)            │
│  Landing · Dashboard · Tasks · Knowledge · Finance   │
│  Approvals · Activity · Settings                     │
└────────────────────┬─────────────────────────────────┘
                     │  REST + SSE (port 8000)
┌────────────────────▼─────────────────────────────────┐
│                    BACKEND (FastAPI)                  │
│  Planner → Executor → Verifier                       │
│  Tools: Files · Email · Calendar · Finance · Docs    │
│  Auth: Google OAuth · Session Middleware              │
│  Speech: faster-whisper (STT) · piper-tts (TTS)      │
│  Blockchain: Transaction adapter                     │
└──────────────────────────────────────────────────────┘
```

## Project Structure

```
A.L.F.R.E.D/
├── backend/
│   ├── main.py                 # FastAPI app, all API routes
│   ├── agent/
│   │   ├── planner.py          # Goal → multi-step plan (LLM)
│   │   ├── executor.py         # Executes plan steps via tools
│   │   ├── verifier.py         # Validates execution results
│   │   ├── replanner.py        # Re-plans on verification failure
│   │   ├── llm.py              # OpenAI client & prompt logic
│   │   └── tools.py            # Tool dispatch for the agent
│   ├── auth/
│   │   └── google.py           # Google OAuth login/callback
│   ├── blockchain/
│   │   └── adapter.py          # Blockchain transaction logging
│   ├── integrations/
│   │   └── google/client.py    # Google Workspace API client
│   ├── models/
│   │   ├── task.py             # Task data model
│   │   └── action.py           # Action/step data model
│   ├── policy/
│   │   └── policy_engine.py    # Approval policy engine
│   ├── storage/
│   │   ├── database.py         # Task persistence (Supabase)
│   │   └── credentials.py      # Credential storage
│   ├── tools/
│   │   ├── files.py            # File search/read/write/analyze
│   │   ├── email.py            # Email send/read
│   │   ├── calendar.py         # Calendar event management
│   │   ├── documents.py        # Document operations
│   │   ├── finance.py          # Finance tracking
│   │   └── tool_registry.py    # Central tool registration
│   ├── tests/                  # Backend test suite
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.jsx     # Landing page with node tree
│   │   │   ├── Workspace.jsx   # Dashboard with goal input
│   │   │   ├── Tasks.jsx       # Task tracking view
│   │   │   ├── Knowledge.jsx   # Document repository + upload
│   │   │   ├── Approvals.jsx   # Human-in-the-loop approvals
│   │   │   ├── Finance.jsx     # Financial overview
│   │   │   ├── Activity.jsx    # Activity log
│   │   │   └── Settings.jsx    # Configuration
│   │   ├── components/
│   │   │   ├── DashboardLayout.jsx
│   │   │   ├── GoalInput.jsx   # Goal composer + file upload
│   │   │   └── ProfileMenu.jsx
│   │   ├── hooks/
│   │   │   ├── useUpload.js    # File upload hook
│   │   │   ├── useAuth.jsx     # Google auth hook
│   │   │   └── taskEvents.js   # SSE task event hook
│   │   └── services/
│   │       └── api.js          # Axios API client
│   ├── .env.local              # VITE_API_URL config
│   └── package.json
├── alfred_workspace/           # Sandbox for uploaded files
├── docs/                       # Design & planning documents
├── demo_data/                  # Sample data for demos
└── requirements.txt            # Root-level Python dependencies
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm**

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SESSION_SECRET=any_random_secret_string
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Start the backend:

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at `http://localhost:5173` (or the next available port).

### 3. Verify

Open the frontend URL in a browser. The dashboard should connect to the backend on port 8000.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tasks` | Create a new task from a natural-language goal |
| `GET` | `/api/tasks/{id}` | Get task status and details |
| `GET` | `/api/tasks/{id}/events` | SSE stream of real-time task events |
| `POST` | `/api/tasks/{id}/approve` | Approve a pending action |
| `POST` | `/api/tasks/{id}/reject` | Reject a pending action |
| `POST` | `/api/files/upload` | Upload a file to the sandbox |
| `GET` | `/api/files` | List all files in the sandbox |
| `GET` | `/api/files/{filename}` | Download/view a specific file |
| `POST` | `/api/speech/transcribe` | Speech-to-text (faster-whisper) |
| `POST` | `/api/speech/synthesize` | Text-to-speech (piper-tts) |
| `GET` | `/auth/google/login` | Initiate Google OAuth |
| `GET` | `/auth/google/callback` | Google OAuth callback |
| `GET` | `/auth/google/status` | Check auth status |

## Agent Pipeline

```
User Goal
  │
  ▼
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Planner  │───▶│ Executor │───▶│ Verifier │
│ (LLM)   │    │ (Tools)  │    │ (LLM)    │
└─────────┘    └──────────┘    └──────────┘
                                     │
                              Pass? ─┤── Yes → Task Complete
                                     │
                                     └── No  → Replanner → loop
```

1. **Planner** — Takes a natural-language goal and produces a structured multi-step plan.
2. **Executor** — Walks the plan step-by-step, dispatching each to the appropriate tool.
3. **Verifier** — Checks whether the execution result satisfies the original goal.
4. **Replanner** — If verification fails, generates a corrected plan and re-executes.

## Tools

| Tool | Capabilities |
|------|-------------|
| **Files** | Search, read, write, append, delete, list, analyze files in the sandbox |
| **Email** | Send and read emails via Google Workspace |
| **Calendar** | Create, read, update calendar events |
| **Documents** | Document operations via Google Docs |
| **Finance** | Expense tracking and financial queries |

## Speech

- **Speech-to-Text**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2-accelerated Whisper inference
- **Text-to-Speech**: [piper-tts](https://github.com/OHF-Voice/piper1-gpl) — Fast, local neural TTS

## Design

The UI follows a **dark industrial / retro-futuristic** aesthetic:
- Monospace typography (`JetBrains Mono`, `IBM Plex Mono`)
- Dark background with subtle grid patterns
- Amber/gold accent colors
- No purple, no neon, no gradients, no glassmorphism

## Testing

```bash
# Backend unit tests
cd backend
pytest

# File capability tests
python test_files_capability.py

# E2E pipeline test
python test_e2e_pipeline.py
```

## Documentation

Detailed design and planning docs are in the [`docs/`](docs/) directory:

- `00_MASTER_PLAN.md` — High-level project plan
- `02_SHARED_CONTRACTS.md` — API contracts between frontend and backend
- `03_DEVELOPER_A_BACKEND.md` — Backend implementation spec
- `04_DEVELOPER_B_FRONTEND.md` — Frontend implementation spec
- `07_UI_DESIGN_NON_VIBE_CODED.md` — UI/UX design rules
- `08_FINAL_INTEGRATION_AND_SPEECH.md` — Speech integration roadmap

## License

This project is part of an academic/personal project. See repository for details.

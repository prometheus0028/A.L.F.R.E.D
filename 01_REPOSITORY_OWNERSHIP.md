# Repository Ownership & File Lock

## Rule

Every significant source file has exactly one owner.

There must never be a file marked as owned by both developers.

## Ownership Matrix

| Path | Owner | Other Developer |
|---|---|---|
| `backend/` | Developer A | NO TOUCH |
| `backend/main.py` | Developer A | NO TOUCH |
| `backend/agent/` | Developer A | NO TOUCH |
| `backend/tools/` | Developer A | NO TOUCH |
| `backend/models/` | Developer A | NO TOUCH |
| `backend/policy/` | Developer A | NO TOUCH |
| `backend/blockchain/` | Developer A | NO TOUCH |
| `backend/storage/` | Developer A | NO TOUCH |
| `demo_data/` | Developer A | NO TOUCH |
| `requirements.txt` | Developer A | NO TOUCH |
| `frontend/` | Developer B | NO TOUCH |
| `frontend/src/` | Developer B | NO TOUCH |
| `frontend/public/` | Developer B | NO TOUCH |
| `frontend/package.json` | Developer B | NO TOUCH |
| `frontend/vite.config.js` | Developer B | NO TOUCH |
| `frontend/index.html` | Developer B | NO TOUCH |
| `frontend/.gitignore` | Developer B | NO TOUCH |
| `frontend/README.md` | Developer B | NO TOUCH |

## Existing Directories

### Developer A

```text
backend/
├── agent/
├── blockchain/
├── models/
├── policy/
├── storage/
├── tools/
└── main.py

demo_data/
├── documents/
├── calendar.json
├── emails.json
└── invoices.json

requirements.txt
```

Developer A may add small files inside these owned directories if genuinely required.

Do not create dozens of abstractions.

### Developer B

```text
frontend/
├── public/
├── src/
├── .gitignore
├── .oxlintrc.json
├── index.html
├── package.json
├── README.md
└── vite.config.js
```

Developer B may add files under `frontend/src/` and `frontend/public/` as required.

## Frozen / Architecture-Sensitive Areas

The following interfaces must remain stable during parallel development:

- REST endpoint paths
- HTTP request/response shapes
- task status values
- action status values
- event names
- event payload shapes
- approval request shape
- verification result shape

See `02_SHARED_CONTRACTS.md`.

## No Cross-Boundary Fixes

Bad:

```text
Developer B notices a backend bug
→ edits backend/main.py
```

Bad:

```text
Developer A thinks the frontend needs a new field
→ edits frontend/src/...
```

Correct:

```text
Developer B:
document the API mismatch

Developer A:
implement backend-side compatibility if possible
```

## Existing Structure Must Be Respected

Do not move the project into a new architecture just because a preferred framework pattern exists.

Do not replace the existing React/Vite frontend wholesale.

Do not replace the backend folder layout wholesale.

The goal is to finish the MVP reliably, not redesign the repository.

## Generated / Local Files

Do not commit:

```text
.env
.env.local
__pycache__/
*.pyc
node_modules/
dist/
.venv/
```

If `.gitignore` changes are needed, each developer changes only the ignore file inside their own owned area.

## Dependency Ownership

Backend dependencies:

```text
requirements.txt
```

Developer A owns it.

Frontend dependencies:

```text
frontend/package.json
```

Developer B owns it.

Never install a frontend dependency into backend configuration or vice versa.

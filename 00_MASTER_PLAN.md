# A.L.F.R.E.D. — Two-Person Implementation Master Plan

## Purpose

This document converts the ALFRED 6-hour MVP specification into a parallel two-person implementation plan for the **existing repository structure**.

The MVP must demonstrate:

> **GOAL → PLAN → ACT → OBSERVE → REPLAN → VERIFY → COMPLETE**

The user gives ALFRED a goal rather than a fixed workflow. The agent dynamically interprets the goal, generates a short plan, chooses registered tools, executes actions, observes results, replans after controlled failure, and independently verifies completion.

The implementation must remain realistic for a 6-hour build.

## Existing Repository — Starting Point

The current repository is already structured approximately as:

```text
A.L.F.R.E.D/
├── backend/
│   ├── agent/
│   ├── blockchain/
│   ├── models/
│   ├── policy/
│   ├── storage/
│   ├── tools/
│   └── main.py
├── demo_data/
│   ├── documents/
│   ├── calendar.json
│   ├── emails.json
│   └── invoices.json
├── docs/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── .oxlintrc.json
│   ├── index.html
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
└── requirements.txt
```

Do **not** reorganize this structure unless a concrete implementation need requires it.

## Two-Person Split

### Developer A — Backend / Agent / Data / Finance

Owns:

```text
backend/
demo_data/
requirements.txt
```

Primary responsibility:

- FastAPI API
- agent state machine
- goal interpretation
- dynamic planner
- tool registry
- executor
- observation handling
- replanning
- verifier
- calendar/email/files/documents/finance tools
- deterministic policy engine
- blockchain adapter/simulator
- task/action models
- persistence/storage
- backend tests

### Developer B — Frontend / UX

Owns:

```text
frontend/
```

Primary responsibility:

- React/Vite application
- goal input
- task status
- live execution timeline
- plan display
- approval interface
- result/evidence view
- errors/loading/empty states
- mock API
- real API adapter
- responsive layout
- frontend visual quality
- frontend tests

## Hard Ownership Rule

There is **no shared source-file ownership**.

Developer A must not edit `frontend/`.

Developer B must not edit `backend/`, `demo_data/`, or `requirements.txt`.

If a cross-boundary issue is discovered, fix it inside your own boundary where possible. If an interface truly must change, stop and document the proposed contract change before changing code.

## Integration Contract

The canonical cross-boundary contract is:

```text
frontend
   |
   | HTTP + SSE
   v
backend
   |
   v
ALFRED agent
```

The frontend must never import backend Python modules.

The backend must never depend on React implementation details.

## MVP Definition of Done

The project is complete when these scenarios work:

### Scenario A — Meeting preparation

User enters:

```text
Prepare me for tomorrow's meeting with Rahul.
```

ALFRED dynamically:

1. understands the goal
2. creates a short plan
3. searches calendar
4. searches email
5. searches project files
6. creates a briefing
7. verifies the briefing
8. reports completion

### Scenario B — Finance

User enters:

```text
Handle the pending invoice if it is within my spending policy.
```

ALFRED:

```text
Invoice
  ↓
Policy
  ↓
Approval
  ↓
Test transaction / simulator
  ↓
Verification
```

The LLM never receives a private key and never directly executes a transaction.

### Scenario C — Recovery

One search intentionally fails.

ALFRED:

```text
Failure
  ↓
Observe
  ↓
Replan
  ↓
Alternative search
  ↓
Recover
  ↓
Verify
```

Maximum replans: 2.

## 6-Hour Priority

1. Working agent loop
2. Dynamic tool selection
3. Meeting demo
4. Verification
5. Replanning
6. Frontend live execution UI
7. Finance approval
8. Blockchain simulator/testnet adapter
9. Visual polish
10. Final integration

Do not add major architecture during the last hour.

## Non-Goals

Do not build:

- arbitrary shell execution
- unrestricted desktop control
- real banking access
- real-money transfers
- multi-agent orchestration
- complex vector memory
- enterprise IAM
- Kubernetes/microservices
- full browser computer-use
- a workflow builder
- unnecessary analytics

## Important Product Principle

The frontend is not a chatbot shell.

It should make this visible:

```text
GOAL
 ↓
UNDERSTAND
 ↓
PLAN
 ↓
ACT
 ↓
OBSERVE
 ↓
ADAPT
 ↓
VERIFY
 ↓
COMPLETE
```

The UI should communicate execution state clearly without visual gimmicks.

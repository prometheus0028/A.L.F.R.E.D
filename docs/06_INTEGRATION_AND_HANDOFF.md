# Integration & Handoff Procedure

## Objective

Connect the independently developed frontend and backend without rewriting either side.

## Development Phases

### Phase 1 — Parallel

Developer A:

```text
backend + demo_data
```

Developer B:

```text
frontend + mock API
```

Both can work simultaneously.

### Phase 2 — Backend Verification

Developer A verifies:

```text
POST /api/tasks
GET /api/tasks/{task_id}
GET /api/tasks/{task_id}/events
POST /api/tasks/{task_id}/approve
POST /api/tasks/{task_id}/reject
```

using curl/Postman/tests.

### Phase 3 — Frontend Verification

Developer B verifies the complete interface using mock events.

The UI must demonstrate:

```text
goal
→ plan
→ execution
→ replanning
→ completion
```

and:

```text
approval_required
→ approve
→ completion
```

### Phase 4 — Merge

Merge:

```text
dev/backend-agent → main
dev/frontend-ui → main
```

No source files should conflict.

## Switching Mock API to Real API

The frontend should have one API abstraction.

Conceptually:

```text
UI
 ↓
task service
 ├── mock implementation
 └── real implementation
```

Do not place `fetch()` calls throughout UI components.

The integration change should primarily be configuration/adapter selection.

## Real API Flow

```text
User
 ↓
React
 ↓
POST /api/tasks
 ↓
FastAPI
 ↓
Task created
 ↓
ALFRED planner
 ↓
Executor
 ↓
Tools
 ↓
SSE events
 ↓
React timeline
```

Finance:

```text
User
 ↓
Goal
 ↓
ALFRED
 ↓
Invoice
 ↓
Policy
 ↓
approval_required event
 ↓
React approval panel
 ↓
POST /approve
 ↓
Backend resumes
 ↓
Blockchain adapter
 ↓
Verifier
 ↓
task_completed
```

## Integration Smoke Test

### Test 1 — Meeting

Input:

```text
Prepare me for tomorrow's meeting with Rahul.
```

Expected visible sequence:

```text
Goal received
Plan created
Calendar search
Meeting found
Email search
Files search
Document creation
Verification
Task complete
```

### Test 2 — Recovery

A search intentionally fails.

Expected:

```text
Tool failed
Replanning
Alternative search
Recovered
Verification
Complete
```

### Test 3 — Finance

Input:

```text
Handle the pending invoice if it is within my spending policy.
```

Expected:

```text
Invoice found
Policy checked
Approval required
```

After Approve:

```text
Transaction submitted
Transaction confirmed
Transaction verified
```

## Integration Bugs

If frontend and backend disagree:

### Wrong

Developer B edits backend.

### Wrong

Developer A edits React.

### Correct

Identify which contract field is wrong.

Then the owner of the relevant boundary implements the fix.

## Final QA

Verify:

```text
[ ] no CORS errors
[ ] API base URL works
[ ] SSE connects
[ ] SSE reconnect does not crash UI
[ ] task status updates
[ ] approval pauses execution
[ ] approval resumes execution
[ ] rejection terminates safely
[ ] meeting briefing is created
[ ] verification works
[ ] replanning works
[ ] transaction result is visible
[ ] no secrets are exposed
[ ] no console errors
[ ] no backend traceback during normal demo
[ ] no frontend overflow
[ ] no vibecoded UI elements remain
```

# ALFRED — Frozen Frontend/Backend Contract

## Purpose

This document is the single source of truth for communication between the backend and frontend.

Both developers implement against these contracts.

Do not casually change them during parallel development.

---

# 1. Task Lifecycle

Allowed task statuses:

```text
created
planning
executing
waiting_approval
verifying
replanning
completed
failed
paused
```

Frontend must render unknown statuses safely rather than crashing.

---

# 2. POST /api/tasks

Creates and starts an autonomous task.

### Request

```json
{
  "goal": "Prepare me for tomorrow's meeting with Rahul."
}
```

### Response

```json
{
  "task_id": "task_001",
  "status": "created",
  "goal": "Prepare me for tomorrow's meeting with Rahul."
}
```

HTTP:

```text
201 Created
```

Errors:

```json
{
  "error": {
    "code": "INVALID_GOAL",
    "message": "A non-empty goal is required."
  }
}
```

---

# 3. GET /api/tasks/{task_id}

Returns current task state.

Example:

```json
{
  "task_id": "task_001",
  "goal": "Prepare me for tomorrow's meeting with Rahul.",
  "status": "executing",
  "current_step": 3,
  "total_steps": 5,
  "plan": [
    {
      "id": "step_1",
      "description": "Find the meeting with Rahul",
      "tool": "calendar.search",
      "status": "completed"
    }
  ],
  "actions": [
    {
      "id": "action_001",
      "tool": "calendar",
      "operation": "search",
      "status": "completed",
      "summary": "Found Rahul project review"
    }
  ],
  "result": null
}
```

---

# 4. POST /api/tasks/{task_id}/approve

Approves a pending consequential action.

Request:

```json
{
  "approval_id": "approval_001"
}
```

Response:

```json
{
  "task_id": "task_001",
  "status": "executing",
  "message": "Approval accepted."
}
```

---

# 5. POST /api/tasks/{task_id}/reject

Rejects a pending consequential action.

Request:

```json
{
  "approval_id": "approval_001",
  "reason": "User rejected the payment."
}
```

Response:

```json
{
  "task_id": "task_001",
  "status": "failed",
  "message": "Payment was rejected by the user."
}
```

---

# 6. Task Object

Canonical fields:

```text
task_id
goal
status
current_step
total_steps
plan
actions
approval
result
created_at
updated_at
```

Do not rename these between frontend and backend.

---

# 7. Plan Step

```json
{
  "id": "step_2",
  "description": "Search relevant emails",
  "tool": "email.search",
  "status": "pending",
  "success_criteria": [
    "relevant messages identified"
  ]
}
```

Allowed step statuses:

```text
pending
running
completed
failed
skipped
```

Plans should normally contain 3–7 steps.

---

# 8. Action Object

```json
{
  "id": "action_003",
  "tool": "email",
  "operation": "search",
  "status": "completed",
  "summary": "Found 4 relevant messages"
}
```

Do not expose sensitive implementation details to the frontend.

---

# 9. Approval Object

```json
{
  "approval_id": "approval_001",
  "type": "payment",
  "status": "pending",
  "title": "Payment requires approval",
  "vendor": "Acme Supplies",
  "amount": 3800,
  "currency": "INR",
  "invoice_id": "INV-1042",
  "policy": {
    "result": "APPROVAL_REQUIRED",
    "vendor_approved": true,
    "within_limit": true,
    "limit": 5000
  }
}
```

Allowed approval statuses:

```text
pending
approved
rejected
expired
```

---

# 10. Result Object

Meeting example:

```json
{
  "type": "meeting_brief",
  "status": "verified",
  "title": "Meeting briefing created",
  "file_name": "meeting_brief.md",
  "summary": "Briefing created and verified.",
  "evidence": [
    "1 calendar event",
    "4 emails",
    "2 documents"
  ]
}
```

Finance example:

```json
{
  "type": "payment",
  "status": "verified",
  "vendor": "Acme Supplies",
  "amount": 3800,
  "currency": "INR",
  "transaction_hash": "0xDEMO...",
  "evidence": [
    "Policy passed",
    "User approved",
    "Transaction confirmed"
  ]
}
```

---

# 11. Agent Events

The backend should stream events through SSE.

Event envelope:

```json
{
  "type": "tool_started",
  "task_id": "task_001",
  "timestamp": "2026-09-01T20:00:00Z",
  "data": {}
}
```

Allowed event types:

```text
goal_received
plan_created
step_started
tool_started
tool_completed
step_completed
verification_started
verification_passed
verification_failed
replanning
approval_required
task_completed
task_failed
```

Examples:

### goal_received

```json
{
  "type": "goal_received",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "goal": "Prepare me for tomorrow's meeting with Rahul."
  }
}
```

### plan_created

```json
{
  "type": "plan_created",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "step_count": 5
  }
}
```

### tool_started

```json
{
  "type": "tool_started",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "tool": "email",
    "operation": "search"
  }
}
```

### tool_completed

```json
{
  "type": "tool_completed",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "tool": "email",
    "operation": "search",
    "summary": "Found 4 relevant messages",
    "success": true
  }
}
```

### replanning

```json
{
  "type": "replanning",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "reason": "No exact document found",
    "attempt": 1,
    "message": "Searching project status documents instead."
  }
}
```

### approval_required

```json
{
  "type": "approval_required",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "approval": {
      "approval_id": "approval_001",
      "type": "payment",
      "vendor": "Acme Supplies",
      "amount": 3800,
      "currency": "INR"
    }
  }
}
```

### task_completed

```json
{
  "type": "task_completed",
  "task_id": "task_001",
  "timestamp": "...",
  "data": {
    "summary": "Meeting briefing created and verified."
  }
}
```

---

# 12. SSE Endpoint

```text
GET /api/tasks/{task_id}/events
```

Content type:

```text
text/event-stream
```

Example:

```text
event: tool_started
data: {"type":"tool_started","task_id":"task_001","data":{"tool":"calendar","operation":"search"}}
```

The frontend must tolerate reconnection.

---

# 13. Error Contract

```json
{
  "error": {
    "code": "TOOL_FAILED",
    "message": "The requested tool could not complete the action.",
    "retryable": true
  }
}
```

Common codes:

```text
INVALID_GOAL
TASK_NOT_FOUND
TOOL_NOT_FOUND
TOOL_FAILED
PLANNING_FAILED
VERIFICATION_FAILED
APPROVAL_REQUIRED
TASK_PAUSED
INTERNAL_ERROR
```

---

# 14. Security Boundary

The frontend may display:

- vendor
- amount
- invoice
- policy result
- transaction status
- transaction hash

The frontend must never receive:

- private keys
- API secrets
- LLM provider secrets
- unrestricted tool credentials

The LLM must never directly execute a financial transaction.

Canonical finance path:

```text
LLM
 ↓
Payment Proposal
 ↓
Deterministic Policy
 ↓
User Approval
 ↓
Blockchain Adapter
 ↓
Verifier
```

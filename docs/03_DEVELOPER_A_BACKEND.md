# Developer A — Backend / Agent / Data Implementation

## Mission

Build the autonomous ALFRED backend inside the existing repository.

You own:

```text
backend/
demo_data/
requirements.txt
```

You do NOT own:

```text
frontend/
```

Do not edit frontend files.

## Starting Repository

The repository already contains:

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

Inspect existing code first. Extend it rather than blindly replacing it.

## Core Requirement

ALFRED must be genuinely goal-driven.

Do NOT implement:

```python
if "Rahul" in goal:
    search_calendar()
    search_email()
    search_files()
```

Instead:

```text
goal
 ↓
LLM interpretation
 ↓
dynamic plan
 ↓
registered tool selection
 ↓
execution
 ↓
observation
 ↓
continue / replan
 ↓
verification
```

The demo data can be fixed. The decision path must remain dynamic.

## Backend Components

Implement only the minimum needed:

```text
backend/agent/
    planner.py
    executor.py
    replanner.py
    verifier.py

backend/tools/
    calendar.py
    email.py
    files.py
    documents.py
    finance.py

backend/policy/
    policy_engine.py

backend/blockchain/
    adapter.py

backend/storage/
    database.py

backend/models/
    task.py
    action.py

backend/main.py
```

Small additional files are acceptable only if they have a clear purpose.

## Agent State Machine

Normal task:

```text
CREATED
 ↓
PLANNING
 ↓
EXECUTING
 ↓
OBSERVING
 ↓
VERIFYING
 ├── SUCCESS → COMPLETED
 └── FAILURE → REPLANNING → EXECUTING
```

Finance:

```text
EXECUTING
 ↓
POLICY_CHECK
 ↓
APPROVAL_REQUIRED
 ↓
WAITING_FOR_USER
 ↓
APPROVED
 ↓
EXECUTING
 ↓
VERIFYING
 ↓
COMPLETED
```

Maximum replans:

```text
2
```

Never create infinite loops.

## Planner

Planner must:

1. interpret the user's goal
2. determine desired outcome
3. identify needed information
4. select available tools
5. order dependencies
6. define success criteria

Plans should normally contain 3–7 steps.

Use structured LLM output.

The available tool names must be explicit.

The LLM can select only registered tools.

## Tool Registry

Register only:

```text
calendar.search
calendar.get_event

email.search
email.read

files.search
files.read
files.create

documents.create

finance.list_pending_invoices
finance.get_invoice
finance.check_policy
finance.propose_payment
```

Never expose arbitrary Python execution.

Never expose shell execution.

## Tool Implementations

Use the existing `demo_data/`.

Calendar:

```text
calendar.search()
calendar.get_event()
```

Email:

```text
email.search()
email.read()
```

Files:

```text
files.search()
files.read()
files.create()
```

Documents:

```text
documents.create()
```

Finance:

```text
finance.list_pending_invoices()
finance.get_invoice()
finance.check_policy()
finance.propose_payment()
```

The tool layer should return structured results rather than raw strings whenever practical.

## Meeting Demo

The backend must support:

```text
Prepare me for tomorrow's meeting with Rahul.
```

The agent should dynamically discover the need for calendar, email, files, and documents.

Expected outcome:

```text
meeting_brief.md
```

Then verify that the file exists.

## Replanning Demo

Force one realistic failure.

For example:

```text
files.search("Rahul project report")
```

returns no exact result.

The agent should observe failure and request an alternative plan from the planner.

Fallback can become:

```text
files.search("project status")
```

Do not hard-code the entire workflow around this failure. The replanner should receive the failed action and observation and produce the alternative.

## Verification

The verifier owns the final completion decision.

Meeting success criteria may include:

```text
meeting_found
context_collected
briefing_created
briefing_verified
```

Finance success criteria may include:

```text
invoice_found
policy_passed
approval_received
transaction_confirmed
transaction_verified
```

Never declare success solely because the planner says it is complete.

## Finance Policy

Policy must be deterministic.

Example:

```json
{
  "max_transaction": 5000,
  "approved_vendors": [
    "Acme Supplies",
    "Office Depot"
  ],
  "require_approval": true
}
```

Results:

```text
ALLOW
DENY
APPROVAL_REQUIRED
```

The LLM cannot override policy.

## Blockchain

Implement the adapter interface so it can support:

```text
real testnet
```

or:

```text
safe simulator
```

if testnet setup is not ready.

Use only test funds.

The LLM must never receive the private key.

The adapter should expose something conceptually like:

```text
submit_transaction(payment_proposal)
verify_transaction(transaction_id)
```

Do not build a wallet application.

## API

Implement the frozen contracts in:

`02_SHARED_CONTRACTS.md`

Required endpoints:

```text
POST /api/tasks
GET /api/tasks/{task_id}
GET /api/tasks/{task_id}/events
POST /api/tasks/{task_id}/approve
POST /api/tasks/{task_id}/reject
```

Use SSE for execution events.

## Events

Emit meaningful events:

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

Do not stream private prompts, secrets, or internal credentials.

## Storage

Use the simplest reliable approach.

SQLite or JSON is acceptable.

Persist enough state to:

- identify task
- preserve plan
- preserve actions
- preserve approval state
- report result

Do not build a complex database architecture.

## Testing

Before handing off to integration, test backend without frontend.

Use pytest and/or a CLI script.

Minimum:

```text
goal accepted
planner returns valid structured plan
registered tool executes
unknown tool rejected
tool failure observed
replanner creates alternative
verification works
policy allows valid invoice
policy denies invalid invoice
approval pauses task
approval resumes task
transaction adapter returns result
transaction verification works
SSE emits events
```

## Definition of Done

Developer A is done when:

```text
POST /api/tasks
```

can start a real autonomous task and the backend can complete Scenario A independently.

Scenario B can pause for approval and resume.

Scenario C demonstrates recovery after failure.

Do not touch frontend files to make this happen.

## Important

If you think a frontend change is required:

1. do not edit it
2. document the required API/interface change
3. keep your backend compatible with the frozen contract if possible

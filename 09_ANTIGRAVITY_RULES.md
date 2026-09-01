# Antigravity Operating Rules — ALFRED

These rules apply to both coding agents.

## Rule 1 — Inspect Before Editing

Before changing code:

1. inspect the existing repository
2. inspect relevant files
3. understand current behavior
4. preserve working functionality unless the task explicitly requires change

Never assume the repository is empty.

## Rule 2 — Respect Ownership

Developer A:

```text
backend/
demo_data/
requirements.txt
```

Developer B:

```text
frontend/
```

Do not edit the other developer's paths.

## Rule 3 — No Cross-Boundary Refactors

Do not refactor the entire application because a different architecture seems cleaner.

Implement the MVP in the existing structure.

## Rule 4 — Contracts Are Frozen

Use:

```text
02_SHARED_CONTRACTS.md
```

as the canonical API/event contract.

Do not silently rename:

```text
task_id
status
plan
actions
approval
result
```

or event names.

## Rule 5 — No Hard-Coded Workflow

Never turn the meeting demo into:

```python
if "Rahul" in goal:
    calendar()
    email()
    files()
    documents()
```

The planner must dynamically determine actions from the goal.

## Rule 6 — Registered Tools Only

The LLM may call only tools explicitly registered by ALFRED.

Never expose:

```text
shell
arbitrary Python
filesystem outside demo environment
private keys
```

## Rule 7 — Verification Matters

Never mark a task complete merely because the planner claims success.

The verifier must check the expected state.

## Rule 8 — Replanning Is Bounded

Maximum:

```text
2 replans
```

If the task cannot safely continue:

```text
paused / failed
```

Do not loop forever.

## Rule 9 — Finance Is Controlled

Never:

```text
LLM → private key
```

Correct:

```text
LLM
 ↓
proposal
 ↓
policy
 ↓
approval
 ↓
adapter
 ↓
verification
```

Use testnet or simulator only.

## Rule 10 — Frontend Must Not Be Vibecoded

For the frontend specifically:

Remove or avoid:

```text
gradient blobs
neon AI effects
glassmorphism
decorative 3D objects
fake metrics
fake charts
excessive cards
emoji
unnecessary icons
constant animations
glowing borders
oversized pills
fake AI confidence
```

The interface must be functional and restrained.

## Rule 11 — No Fake Data

Do not display invented values just to make the dashboard look populated.

If data is demo data, make it meaningful and consistent with `demo_data/`.

## Rule 12 — No Overengineering

Prefer:

```text
simple
small
testable
deterministic
```

Avoid unnecessary:

```text
microservices
message queues
vector databases
complex agent frameworks
multiple agents
enterprise IAM
```

## Rule 13 — Keep the Diff Focused

Each coding task should change only what is necessary.

Before finishing:

```bash
git diff --stat
git status
```

Check that only owned files were changed.

## Rule 14 — Do Not Hide Errors

Do not swallow exceptions merely to make the demo appear successful.

Return structured failures so ALFRED can observe and replan.

## Rule 15 — Demo Reliability Beats Feature Count

If time is running out:

prioritize:

```text
meeting demo
replanning
verification
approval
```

over optional features.

## Rule 16 — Stop Adding Architecture

Once the core loop works:

```text
GOAL → PLAN → ACT → OBSERVE → REPLAN → VERIFY
```

do not introduce major architectural changes.

## Final Instruction

Build the smallest reliable system that demonstrates the ALFRED thesis:

> **Give ALFRED a goal, not a workflow. It figures out the steps, executes across digital tools, adapts when things fail, verifies the result, and asks for approval when an action has real consequences.**

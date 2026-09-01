# A.L.F.R.E.D. — 6-Hour Autonomous MVP Specification

> **Autonomous Logical Framework for Reasoning, Execution & Decision-making**
>
> **Goal:** Build a genuinely autonomous, demonstrable ALFRED MVP in **6 hours or less**.
>
> **Core principle:** **Give ALFRED a goal, not a workflow.**
>
> This document intentionally removes features that are impressive on paper but risky to implement within a short hackathon window.

---

# 1. MVP Vision

ALFRED is a small autonomous digital worker.

The user gives ALFRED a natural-language objective such as:

> **"Prepare me for tomorrow's meeting with Rahul."**

ALFRED independently:

1. Understands the goal
2. Creates a short plan
3. Searches available information
4. Decides which tools are useful
5. Executes multiple actions
6. Observes results
7. Verifies the outcome
8. Replans if something fails
9. Presents a concise completion report

For the 6-hour MVP, ALFRED should operate inside a **controlled local/demo environment** rather than attempting unrestricted access to the user's entire computer.

The system should feel autonomous because the user provides only the goal.

---

# 2. What We Are Actually Building

## Build this

```text
Natural-language Goal
        ↓
Goal Parser
        ↓
Planner
        ↓
Tool Selection
        ↓
Tool Execution
        ↓
Observation
        ↓
Verification
        ↓
Replan if necessary
        ↓
Final Result
```

## Do NOT build this yet

- Fully autonomous desktop control
- Arbitrary shell execution
- Production banking access
- Real money transfers
- Dozens of integrations
- Complex multi-agent systems
- Long-term learned workflows
- Advanced vector memory
- Full enterprise IAM
- Full account abstraction infrastructure
- Complicated browser vision automation
- Large distributed architecture

The MVP should demonstrate the **architecture**, not attempt to solve every problem.

---

# 3. The Core Product

ALFRED is not primarily a chatbot.

A chatbot:

```text
User → Question → Answer
```

A workflow automation:

```text
Trigger → Fixed Steps → Result
```

ALFRED:

```text
Goal
 ↓
Plan
 ↓
Choose tools
 ↓
Act
 ↓
Observe
 ↓
Verify
 ↓
Replan
 ↓
Complete
```

The user does not specify the intermediate steps.

---

# 4. The Best 6-Hour Demo

The strongest demo should be a single end-to-end task.

## User goal

> **"Prepare me for my meeting with Rahul tomorrow."**

ALFRED should automatically discover that it needs:

```text
Calendar
Email
Documents / Files
```

Then execute:

```text
1. Find Rahul's meeting tomorrow
2. Extract meeting time and context
3. Search relevant emails
4. Search relevant project documents
5. Identify the most recent useful information
6. Generate a meeting briefing
7. Save the briefing
8. Verify that the briefing exists
9. Report completion
```

The user never says:

> "Search Calendar."

The user only gives the goal.

This is enough to demonstrate genuine autonomy.

---

# 5. Second Demo — Autonomous Finance Task

The fintech/blockchain part should be a separate short scenario.

User:

> **"Handle the pending invoice if it is within my spending policy."**

ALFRED:

```text
Find invoice
      ↓
Extract amount + vendor
      ↓
Check policy
      ↓
If within policy
      ↓
Request approval
      ↓
Execute controlled test transaction
      ↓
Verify transaction
      ↓
Show evidence
```

Example:

```text
Invoice found

Vendor:
Acme Supplies

Amount:
₹3,800

Policy:
Maximum ₹5,000
Approved vendor

Policy result:
ALLOWED

User approval required.

[Approve] [Reject]
```

After approval:

```text
Transaction submitted
        ↓
Blockchain confirmation
        ↓
Transaction verified
        ↓
Task complete
```

Use **testnet / mock funds only**.

---

# 6. MVP Features

The MVP should have exactly these core capabilities.

## Feature 1 — Goal Input

A single natural-language input:

```text
What should ALFRED accomplish?

[ Prepare me for tomorrow's meeting with Rahul ]
```

Button:

```text
Run
```

No workflow builder is required.

---

# 7. Feature 2 — Goal Understanding

The LLM converts the goal into a structured task.

Example:

```json
{
  "goal": "Prepare me for tomorrow's meeting with Rahul",
  "objective": "Create a useful meeting briefing",
  "constraints": [],
  "required_outcome": "Briefing document saved"
}
```

Keep this structured and simple.

---

# 8. Feature 3 — Dynamic Planning

The LLM creates a short plan.

Example:

```json
{
  "steps": [
    {
      "id": 1,
      "description": "Find tomorrow's meeting with Rahul",
      "tool": "calendar"
    },
    {
      "id": 2,
      "description": "Find relevant emails",
      "tool": "email"
    },
    {
      "id": 3,
      "description": "Find latest project document",
      "tool": "files"
    },
    {
      "id": 4,
      "description": "Generate meeting briefing",
      "tool": "documents"
    },
    {
      "id": 5,
      "description": "Verify briefing exists",
      "tool": "files"
    }
  ]
}
```

The important part:

**The plan is generated from the goal.**

Do not hard-code the exact sequence into the backend.

---

# 9. Feature 4 — Small Tool Registry

Only build 4–5 tools.

## Tool 1 — Calendar

Capabilities:

```text
calendar.search()
calendar.get_event()
```

Data can come from a local JSON database.

Example:

```json
{
  "title": "Rahul — Project Review",
  "date": "2026-09-02",
  "time": "11:00",
  "attendees": ["Rahul", "Sarthak"],
  "project": "ALFRED"
}
```

---

# 10. Tool 2 — Email

Capabilities:

```text
email.search()
email.read()
```

Use a controlled local dataset.

Example:

```json
{
  "sender": "rahul@example.com",
  "subject": "ALFRED architecture review",
  "body": "Let's review the agent architecture tomorrow.",
  "date": "2026-09-01"
}
```

The agent should search this dataset based on the task.

---

# 11. Tool 3 — Files

Capabilities:

```text
files.search()
files.read()
files.create()
```

Use a local `demo_data/` directory.

Example:

```text
demo_data/
├── ALFRED_architecture.md
├── ALFRED_requirements.md
├── meeting_notes.md
└── project_status.md
```

ALFRED searches these files using filenames and/or simple text matching.

---

# 12. Tool 4 — Documents

Capabilities:

```text
documents.create()
```

The agent can create a Markdown or HTML briefing.

Example output:

```text
ALFRED Meeting Brief

Meeting:
Rahul — Project Review

Time:
11:00 AM

Recent Discussion:
...

Latest Project Status:
...

Key Topics:
1. Agent execution
2. Policy engine
3. Blockchain demo

Recommended Questions:
...
```

Do not build a complicated document editor.

---

# 13. Tool 5 — Finance

Create a tiny simulated finance environment.

Capabilities:

```text
finance.list_pending_invoices()
finance.get_invoice()
finance.check_policy()
finance.propose_payment()
```

Example dataset:

```json
{
  "invoice_id": "INV-1042",
  "vendor": "Acme Supplies",
  "amount": 3800,
  "currency": "INR",
  "approved_vendor": true,
  "status": "pending"
}
```

---

# 14. Blockchain Feature

For the 6-hour version, blockchain should demonstrate **programmable authority**, not become an entire wallet product.

Use one controlled transaction.

Flow:

```text
Finance
   ↓
Payment proposal
   ↓
Policy check
   ↓
User approval
   ↓
Blockchain transaction
   ↓
Confirmation
```

If testnet setup is already available, execute a testnet transaction.

If not, implement a **blockchain transaction simulator** first and make the interface compatible with a real blockchain adapter.

Do not allow real funds.

---

# 15. Policy Engine

The policy engine should be simple and deterministic.

Example configuration:

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

Policy function:

```text
check_payment(vendor, amount)
```

Possible results:

```text
ALLOW
DENY
APPROVAL_REQUIRED
```

Example:

```text
Vendor:
Acme Supplies

Amount:
₹3,800

Maximum:
₹5,000

Vendor approved:
YES

Result:
APPROVAL_REQUIRED
```

---

# 16. Critical Security Principle

The LLM must not directly execute financial transactions.

Architecture:

```text
LLM
 ↓
Payment Proposal
 ↓
Policy Engine
 ↓
Approval
 ↓
Execution Adapter
 ↓
Blockchain
```

The LLM should never receive a private key.

For the MVP, keep blockchain credentials entirely outside the LLM context.

---

# 17. Feature 6 — Approval Gate

When a consequential action occurs, pause the agent.

UI:

```text
┌──────────────────────────────────────────┐
│ APPROVAL REQUIRED                        │
│                                          │
│ Pay ₹3,800 to Acme Supplies              │
│                                          │
│ Reason                                   │
│ Pending invoice INV-1042                 │
│                                          │
│ Policy                                   │
│ ✓ Vendor approved                        │
│ ✓ Under ₹5,000 limit                    │
│                                          │
│ [ Reject ]                  [ Approve ]  │
└──────────────────────────────────────────┘
```

After approval:

```text
Resume task
```

This is an important demonstration of controlled autonomy.

---

# 18. Feature 7 — Live Execution Timeline

Show the agent's progress.

Example:

```text
PREPARING MEETING BRIEF

✓ Understanding goal
✓ Planning task

✓ Searching calendar
✓ Meeting found

✓ Searching email
✓ 4 relevant messages found

✓ Searching files
✓ Latest project report found

● Generating briefing

○ Verification
```

This makes the autonomous behavior visible.

---

# 19. Feature 8 — Verification

Every major task should have a verification function.

Example:

```text
documents.create()
        ↓
files.exists()
        ↓
SUCCESS
```

Meeting briefing verification:

```text
Expected:
meeting_brief.md exists

Actual:
meeting_brief.md exists

Status:
VERIFIED
```

Finance verification:

```text
Expected:
transaction confirmed

Actual:
transaction receipt found

Status:
VERIFIED
```

---

# 20. Feature 9 — Simple Replanning

This is important because it makes the agent feel autonomous.

Create one intentional failure.

Example:

The planner asks:

```text
files.search("Rahul project report")
```

The demo dataset contains no exact matching filename.

The tool returns:

```text
No exact result.
```

ALFRED should not stop immediately.

It should generate a fallback:

```text
No exact file found.

Replanning:
Search project status documents
```

Then:

```text
files.search("project status")
```

Finds:

```text
ALFRED_project_status.md
```

This demonstrates:

```text
Failure
 ↓
Observation
 ↓
Replanning
 ↓
Recovery
```

This is far more valuable than adding five more superficial features.

---

# 21. Feature 10 — Final Result

At the end:

```text
TASK COMPLETE

Prepare me for tomorrow's meeting with Rahul

✓ Meeting found
✓ Relevant emails analysed
✓ Project documents reviewed
✓ Meeting briefing created
✓ Briefing verified

Created:
meeting_brief.md

Sources:
4 emails
2 documents
1 calendar event

Time:
18.4 seconds
```

For finance:

```text
PAYMENT COMPLETE

✓ Invoice identified
✓ Policy checked
✓ User approved
✓ Transaction submitted
✓ Transaction verified

Amount:
₹3,800

Vendor:
Acme Supplies

Transaction:
0x...
```

---

# 22. Memory — Keep It Extremely Simple

Do not build a vector database in the first 6 hours.

Use a small JSON or SQLite memory store.

Example:

```json
{
  "user_preferences": {
    "meeting_duration": 30,
    "preferred_report_format": "markdown"
  },
  "people": {
    "Rahul": {
      "role": "project teammate"
    }
  }
}
```

The first memory feature should simply prove that ALFRED can retain useful information between tasks.

Example:

User:

> "Remember that Rahul is the project lead."

Later:

> "Prepare me for my meeting with the project lead."

ALFRED can resolve:

```text
project lead → Rahul
```

This is optional if time is tight.

---

# 23. Do Not Build Full Computer Vision

For a 6-hour MVP:

**Do not build general-purpose computer vision control.**

Instead use:

```text
LLM
 ↓
Tool calls
 ↓
Controlled applications
```

If you already have browser automation available, add one controlled browser task.

But browser automation should be an enhancement, not a dependency for the MVP.

---

# 24. Optional Browser Feature

If the core system is finished early, add:

```text
browser.search()
browser.open()
browser.extract()
```

Example goal:

> "Find the current price of the product mentioned in this email."

ALFRED:

```text
Email
 ↓
Extract product
 ↓
Browser
 ↓
Search
 ↓
Extract result
 ↓
Return finding
```

This adds another environment without requiring full computer control.

---

# 25. Recommended Tech Stack

## Frontend

Use the team's existing preferred stack if already configured.

Otherwise:

```text
React
Vite
Tailwind CSS
```

## Backend

```text
Python
FastAPI
```

## Agent

```text
LLM with structured tool calling
```

## Storage

For speed:

```text
SQLite
```

or:

```text
JSON
```

Use SQLite if task persistence is needed.

## Blockchain

```text
EVM-compatible testnet
```

Optional adapter:

```text
Viem
```

If blockchain deployment is not ready:

```text
Blockchain simulator
```

with the same interface as the real adapter.

---

# 26. Simplified Architecture

```text
                 USER
                  │
                  ▼
          ┌────────────────┐
          │  ALFRED UI     │
          │                │
          │ Goal + Status  │
          └───────┬────────┘
                  │
                  ▼
          ┌────────────────┐
          │ ALFRED CORE    │
          │                │
          │ Goal Parser    │
          │ Planner        │
          │ Executor       │
          │ Replanner      │
          └───────┬────────┘
                  │
            Tool Selection
                  │
       ┌──────────┼───────────┐
       ▼          ▼           ▼
   Calendar     Email       Files
       │          │           │
       └──────────┼───────────┘
                  │
                  ▼
             Documents
                  │
                  ▼
              Verifier
                  │
             ┌────┴────┐
             │         │
          SUCCESS    FAILURE
             │         │
             ▼         ▼
          Complete   Replan
                         │
                         └──→ Executor


Financial flow:

            ALFRED
               │
               ▼
        Payment Proposal
               │
               ▼
         Policy Engine
               │
          ┌────┴────┐
          │         │
        DENY      ALLOW
                    │
                    ▼
              User Approval
                    │
                    ▼
             Blockchain Adapter
                    │
                    ▼
                Verifier
```

---

# 27. Backend Structure

Keep it small.

```text
backend/
│
├── main.py
│
├── agent/
│   ├── planner.py
│   ├── executor.py
│   ├── replanner.py
│   └── verifier.py
│
├── tools/
│   ├── calendar.py
│   ├── email.py
│   ├── files.py
│   ├── documents.py
│   └── finance.py
│
├── policy/
│   └── policy_engine.py
│
├── blockchain/
│   └── adapter.py
│
├── storage/
│   └── database.py
│
└── models/
    ├── task.py
    └── action.py
```

Do not create dozens of files for abstractions that are not needed yet.

---

# 28. Agent State Machine

Use a simple state machine.

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
   │
   ├── SUCCESS → COMPLETED
   │
   └── FAILURE → REPLANNING
                         │
                         └── EXECUTING
```

Financial task:

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

---

# 29. Action Object

Every action should be represented consistently.

Example:

```json
{
  "id": "action_003",
  "tool": "email",
  "operation": "search",
  "parameters": {
    "query": "Rahul ALFRED project"
  },
  "status": "completed",
  "result": {
    "count": 4
  }
}
```

This allows the UI to display the agent's execution history.

---

# 30. Task Object

```json
{
  "id": "task_001",
  "goal": "Prepare me for tomorrow's meeting with Rahul",
  "status": "executing",
  "current_step": 3,
  "total_steps": 5,
  "plan": [],
  "actions": []
}
```

---

# 31. Planner Rules

The planner should produce **short plans**.

Target:

```text
3–7 steps
```

Avoid plans with 20+ actions.

The planner should:

1. Identify the desired outcome
2. Identify required information
3. Select available tools
4. Order dependent operations
5. Define success criteria

Example:

```json
{
  "goal": "Prepare meeting briefing",
  "success_criteria": [
    "meeting identified",
    "relevant context found",
    "briefing created",
    "briefing verified"
  ]
}
```

---

# 32. Tool Selection

Do not expose every implementation detail to the LLM.

Give it a compact tool description.

Example:

```text
calendar.search:
Find calendar events matching a query.

email.search:
Search messages by sender, subject or keywords.

files.search:
Search available project files.

documents.create:
Create a new briefing document.

finance.list_pending_invoices:
List pending invoices.

finance.check_policy:
Check whether a payment is allowed.
```

---

# 33. Preventing Hallucinated Actions

The model must only be able to call registered tools.

```text
AVAILABLE TOOLS

calendar.search
email.search
email.read
files.search
files.read
documents.create
finance.list_pending_invoices
finance.check_policy
finance.propose_payment
```

If a tool does not exist:

```text
The agent cannot execute that action.
```

Do not allow arbitrary Python execution through the LLM.

---

# 34. Demo Data

Create realistic but small demo data.

```text
demo_data/
│
├── emails.json
├── calendar.json
├── invoices.json
│
└── documents/
    ├── ALFRED_architecture.md
    ├── ALFRED_project_status.md
    ├── meeting_notes.md
    └── roadmap.md
```

The data should be internally connected.

For example:

```text
Calendar:
Rahul — ALFRED Review

Email:
Rahul discusses ALFRED architecture

Document:
ALFRED project status

Invoice:
Acme Supplies
```

This makes the agent's decisions meaningful.

---

# 35. Recommended Demo Story

## Scene 1 — Goal

User:

> "Prepare me for tomorrow's meeting with Rahul."

## Scene 2 — Planning

Show:

```text
I need to:
1. Find the meeting
2. Gather relevant communication
3. Find the latest project information
4. Create a briefing
5. Verify the result
```

## Scene 3 — Autonomous execution

The UI updates live:

```text
Calendar ✓
Email ✓
Files ✓
Documents ●
Verification ○
```

## Scene 4 — Recovery

Force one search to fail.

Show:

```text
No exact document found.

Replanning...
Searching project status documents...
```

Then:

```text
Recovered ✓
```

## Scene 5 — Result

```text
Meeting briefing created and verified.
```

## Scene 6 — Finance

User:

> "Handle the pending invoice if it is within my policy."

ALFRED:

```text
Invoice found
Policy checked
Approval required
```

User clicks:

```text
Approve
```

Transaction executes.

## Scene 7 — Proof

```text
✓ Policy passed
✓ User approved
✓ Transaction confirmed
✓ Task verified
```

This tells a complete story.

---

# 36. What Makes This Truly Autonomous

The MVP is autonomous if ALFRED can:

```text
Receive only a goal
        ↓
Determine necessary information
        ↓
Select tools
        ↓
Execute multiple steps
        ↓
Interpret results
        ↓
Change strategy after failure
        ↓
Determine whether the outcome was achieved
```

It is NOT autonomous if the backend simply does:

```python
if "Rahul" in goal:
    search_calendar()
    search_email()
    search_files()
    create_document()
```

Avoid this.

The demo data can be fixed.

The **decision process must be dynamic**.

---

# 37. What Can Be Hard-Coded

It is acceptable to hard-code:

- Demo datasets
- Tool implementations
- Policy rules
- UI structure
- Available tools
- Test accounts
- Test blockchain contract
- Safe demo environment

It is NOT ideal to hard-code:

- The exact plan for each natural-language goal
- The exact tool sequence
- The exact recovery strategy
- The exact final response

Those should be generated dynamically.

---

# 38. What Should Be LLM-Driven

Use the LLM for:

### Goal interpretation

```text
What does the user want?
```

### Planning

```text
What steps are necessary?
```

### Tool selection

```text
Which tool should be used?
```

### Data synthesis

```text
What information is relevant?
```

### Replanning

```text
The previous action failed. What should happen next?
```

### Final summary

```text
What was accomplished?
```

Do NOT use the LLM for:

- Policy enforcement
- Private-key management
- Direct database mutation without tools
- Financial authorization
- Security decisions that can be deterministic

---

# 39. 6-Hour Build Plan

## Hour 0–1 — Foundation

Build:

- React/Vite UI
- FastAPI backend
- Basic `/task` endpoint
- LLM connection
- Demo data
- Tool registry

Deliverable:

```text
User enters goal
        ↓
Backend receives it
        ↓
LLM responds
```

---

## Hour 1–2 — Agent Loop

Implement:

```text
goal
 ↓
planner
 ↓
executor
 ↓
tool result
 ↓
next step
```

Get the meeting task working.

Deliverable:

```text
One natural-language goal
→ multiple dynamic tool calls
→ result
```

---

## Hour 2–3 — Real Autonomy

Add:

- Planner state
- Action objects
- Execution timeline
- Verification
- Replanning

Force one tool failure.

Deliverable:

```text
Failure
 ↓
Replan
 ↓
Recovery
```

---

## Hour 3–4 — Fintech

Add:

- Invoice dataset
- Policy engine
- Payment proposal
- Approval UI
- Finance tool

Deliverable:

```text
Goal
→ Invoice
→ Policy
→ Approval
```

---

## Hour 4–5 — Blockchain

If testnet infrastructure is available:

```text
Approval
 ↓
Transaction
 ↓
Confirmation
```

Otherwise:

```text
Approval
 ↓
Blockchain simulator
 ↓
Fake transaction hash
 ↓
Verified result
```

The UI and backend should keep the same adapter interface so the simulator can later be replaced by a real blockchain implementation.

---

## Hour 5–6 — Polish + Demo

Focus on:

- Clean UI
- Execution timeline
- Approval modal
- Final result
- Error handling
- Demo reset button
- Stable demo data
- Repeatable demo

Do NOT add major new architecture during the final hour.

---

# 40. Suggested UI

## Main screen

```text
┌─────────────────────────────────────────────────┐
│ ALFRED                                  ● READY │
├─────────────────────────────────────────────────┤
│                                                 │
│ What should I accomplish?                      │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ Prepare me for tomorrow's meeting with     │ │
│ │ Rahul                                      │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│                     [ RUN TASK ]                │
│                                                 │
├─────────────────────────────────────────────────┤
│ EXECUTION                                      │
│                                                 │
│ ✓ Goal understood                              │
│ ✓ Plan created                                 │
│ ✓ Calendar searched                            │
│ ✓ Email searched                               │
│ ● Creating briefing                            │
│ ○ Verification                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

# 41. Approval UI

```text
┌─────────────────────────────────────────────┐
│ PAYMENT REQUIRES APPROVAL                   │
│                                             │
│ Acme Supplies                               │
│ ₹3,800 INR                                  │
│                                             │
│ Invoice: INV-1042                           │
│                                             │
│ Policy                                     │
│ ✓ Vendor approved                           │
│ ✓ Under ₹5,000 limit                       │
│                                             │
│ [ REJECT ]                 [ APPROVE ]      │
└─────────────────────────────────────────────┘
```

---

# 42. Activity Log

Display:

```text
20:41:02  Goal received
20:41:03  Plan generated
20:41:03  Calendar search
20:41:04  Meeting identified
20:41:05  Email search
20:41:06  4 relevant emails found
20:41:07  File search
20:41:07  No exact result
20:41:08  Replanning
20:41:09  Project status found
20:41:11  Briefing created
20:41:11  Verification passed
```

This makes the system look much more like an agent.

---

# 43. Optional Features If Ahead of Schedule

Only add these after the core demo works.

## Optional 1 — Browser Search

```text
browser.search()
browser.extract()
```

## Optional 2 — Task History

```text
Previous Tasks

✓ Meeting briefing
✓ Expense review
✓ Invoice approval
```

## Optional 3 — Simple Memory

```text
Remember:
Rahul = project lead
```

## Optional 4 — Dry Run

```text
Preview plan before execution.
```

## Optional 5 — Pause / Resume

```text
Pause task
Resume task
```

## Optional 6 — Multiple Goals

Allow the user to submit another goal without restarting the backend.

---

# 44. Features to Explicitly Reject for the 6-Hour Version

Do not spend time on:

```text
❌ General desktop computer-use
❌ General-purpose vision agent
❌ Multi-agent system
❌ Advanced vector memory
❌ Real banking integrations
❌ Real money
❌ Enterprise authentication
❌ Complex smart-account architecture
❌ Dozens of API integrations
❌ Full browser agent
❌ Autonomous shell access
❌ Complex workflow editor
❌ Custom LLM training
❌ Massive database architecture
❌ Advanced analytics
```

These are roadmap features.

---

# 45. Technical Quality Requirements

Even though this is a rapid MVP:

### Must have

- Structured tool calls
- Clear task state
- Deterministic policy engine
- Approval gate
- Verification
- Error handling
- No direct private-key access
- No arbitrary code execution
- Repeatable demo environment

### Nice to have

- Streaming execution updates
- Persistent task history
- Browser integration
- Memory
- Real testnet transaction

---

# 46. Security Model

The minimum security architecture:

```text
             LLM
              │
              ▼
        Tool Proposal
              │
              ▼
       Permission Check
              │
        ┌─────┴─────┐
        │           │
       SAFE       SENSITIVE
        │           │
        ▼           ▼
     Execute     Approval
                    │
                    ▼
                 Execute
```

Financial actions:

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
```

Never:

```text
LLM → Private Key
```

---

# 47. Failure Strategy

For every tool:

```text
try action
 ↓
observe result
 ↓
if success:
    continue
else:
    ask planner for alternative
```

Limit replanning:

```text
MAX_REPLANS = 2
```

If the agent still cannot complete the task:

```text
TASK PAUSED

I could not safely complete this step.

Reason:
No relevant project document was found.

[Try Again]
[Stop]
```

Do not allow infinite agent loops.

---

# 48. Verification Strategy

Every plan should include success criteria.

Example:

```json
{
  "success_criteria": [
    "meeting_found",
    "context_collected",
    "briefing_created",
    "briefing_exists"
  ]
}
```

The verifier checks these independently.

This creates:

```text
Planner says:
"I think we are done."

Verifier says:
"Is the expected state actually true?"
```

The verifier should have authority over task completion.

---

# 49. The Most Important Demo Principle

Do not make the demo look like:

```text
Chatbot
 ↓
Tool
 ↓
Tool
 ↓
Tool
```

Make it look like:

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

The **adaptation** and **verification** steps are what make the project feel autonomous.

---

# 50. Final MVP Feature List

The finished 6-hour ALFRED should have:

```text
CORE
[✓] Natural-language goals
[✓] Goal interpretation
[✓] Dynamic planning
[✓] Dynamic tool selection
[✓] Multi-step execution
[✓] Execution state
[✓] Live activity timeline

AUTONOMY
[✓] Tool result observation
[✓] Verification
[✓] Replanning
[✓] Controlled failure recovery

TOOLS
[✓] Calendar
[✓] Email
[✓] Files
[✓] Documents
[✓] Finance

FINTECH
[✓] Invoice discovery
[✓] Policy engine
[✓] Payment proposal
[✓] Human approval
[✓] Test transaction / blockchain adapter
[✓] Transaction verification

SAFETY
[✓] Tool allowlist
[✓] No arbitrary code execution
[✓] No private-key exposure
[✓] Deterministic financial policy
[✓] Approval for sensitive actions
[✓] Replan limit

UX
[✓] Goal input
[✓] Live execution
[✓] Approval modal
[✓] Final result
[✓] Evidence / activity log
```

---

# 51. Definition of Done

The project is done when this works reliably:

## Scenario A

User:

> **"Prepare me for tomorrow's meeting with Rahul."**

ALFRED automatically:

```text
Calendar
 ↓
Email
 ↓
Files
 ↓
Document creation
 ↓
Verification
 ↓
Final briefing
```

with no user intervention.

## Scenario B

User:

> **"Handle the pending invoice if it is within my spending policy."**

ALFRED automatically:

```text
Invoice
 ↓
Policy
 ↓
Approval
 ↓
Transaction
 ↓
Verification
```

The user only intervenes at the appropriate authorization boundary.

## Scenario C

A tool intentionally fails.

ALFRED:

```text
Detects failure
 ↓
Replans
 ↓
Uses alternative approach
 ↓
Completes task
```

If all three scenarios work, the MVP demonstrates the central ALFRED thesis.

---

# 52. Final Product Positioning

ALFRED should be presented as:

> **A lightweight autonomous execution layer that turns user goals into verified actions across digital tools, while keeping authority and execution under explicit control.**

Not:

> "An AI chatbot that can call APIs."

Not:

> "A blockchain payment bot."

Not:

> "A browser automation script."

The differentiating loop is:

```text
GOAL
 ↓
PLAN
 ↓
ACT
 ↓
OBSERVE
 ↓
REPLAN
 ↓
VERIFY
```

And the fintech safety principle is:

```text
REASONING ≠ AUTHORITY
```

---

# 53. Final 10-Second Pitch

> **Give ALFRED a goal, not a workflow. It figures out the steps, executes across your digital tools, adapts when things fail, verifies the result, and asks for your approval when an action has real consequences.**

---

# 54. Final IDE Instruction

Treat this document as the **MVP source of truth**.

Implement the smallest reliable system that satisfies the Definition of Done.

Prioritise:

1. Autonomous planning
2. Dynamic tool selection
3. Multi-step execution
4. Observation
5. Replanning
6. Verification
7. Financial policy
8. Approval
9. Controlled blockchain execution
10. Clean demonstration

Do not expand the architecture until the primary end-to-end workflow works.

**If forced to choose between another feature and making the agent loop reliable, choose the agent loop.**

The goal is not to build the biggest AI agent.

The goal is to build a small agent that **actually accomplishes a goal autonomously.**

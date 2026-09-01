# ALFRED — Test & Demo Plan

## Goal

The demo must prove autonomy rather than merely show API calls.

The story is:

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

## Scenario A — Meeting Preparation

Input:

```text
Prepare me for tomorrow's meeting with Rahul.
```

### Expected behavior

ALFRED dynamically determines useful tools.

Possible plan:

```text
Find meeting
Gather relevant communication
Find latest project information
Create briefing
Verify briefing
```

The exact tool order should come from the agent, not a hard-coded `if/else` workflow.

### Expected evidence

```text
calendar event found
relevant emails found
project documents found
meeting briefing created
briefing verified
```

## Scenario B — Controlled Failure Recovery

Cause one search to fail.

Expected UI:

```text
Searching project documents
        ↓
No exact result
        ↓
Replanning
        ↓
Searching project status
        ↓
Relevant document found
        ↓
Continue
```

This is a core proof point.

## Scenario C — Finance

Input:

```text
Handle the pending invoice if it is within my spending policy.
```

Expected:

```text
Invoice discovered
 ↓
Policy evaluated
 ↓
Approval required
 ↓
User approves
 ↓
Test transaction submitted
 ↓
Transaction verified
```

## Scenario D — Finance Denial

Use an invoice that violates policy.

Expected:

```text
Invoice discovered
 ↓
Policy evaluated
 ↓
DENY
 ↓
No transaction
```

The LLM must not override the policy engine.

## Backend Tests

Minimum:

```text
[ ] planner returns valid schema
[ ] planner uses only registered tools
[ ] executor executes tool
[ ] unknown tool is rejected
[ ] failed tool returns structured failure
[ ] replanner receives failure observation
[ ] replanner returns valid alternative
[ ] maximum replan count enforced
[ ] verifier checks actual state
[ ] task does not complete on failed verification
[ ] policy allows valid invoice
[ ] policy denies invalid invoice
[ ] approval pauses task
[ ] approval resumes task
[ ] rejection stops sensitive action
[ ] blockchain simulator works
[ ] transaction verification works
[ ] SSE events emitted
```

## Frontend Tests

```text
[ ] goal input works
[ ] run button disabled when goal empty
[ ] loading state works
[ ] plan appears
[ ] timeline updates
[ ] current step is visually clear
[ ] replanning state appears
[ ] approval panel appears
[ ] approve button works
[ ] reject button works
[ ] result appears
[ ] failure state appears
[ ] long text wraps correctly
[ ] no horizontal overflow
[ ] no console errors
```

## Integration Tests

### Test 1

```text
React
→ POST /api/tasks
→ task created
→ SSE connected
→ events render
→ task completed
```

### Test 2

```text
React
→ finance goal
→ approval_required
→ approval UI
→ POST /approve
→ task resumes
→ transaction verified
```

### Test 3

```text
tool failure
→ replanning event
→ alternate action
→ successful result
```

## Demo Reset

Provide a simple reset mechanism for the demo.

It may be a frontend control if it maps to a backend reset endpoint, or a backend/demo-data reset procedure.

It must not mutate arbitrary user data.

## Demo Timing

Aim for:

```text
meeting demo: < 60 seconds
finance demo: < 45 seconds
recovery moment: visible within the meeting demo
```

Do not optimize for artificial speed at the expense of visible reasoning/execution.

## Final Demo Script

### 1. Goal

Say:

> "I don't tell ALFRED which applications to use. I only give it the goal."

Enter:

```text
Prepare me for tomorrow's meeting with Rahul.
```

### 2. Plan

Show the generated plan.

### 3. Execute

Let the timeline show:

```text
calendar
email
files
documents
```

### 4. Failure

Allow the controlled search failure.

Show:

```text
Replanning…
```

Then recovery.

### 5. Verify

Show:

```text
Briefing created
Verification passed
```

### 6. Finance

Enter:

```text
Handle the pending invoice if it is within my spending policy.
```

### 7. Approval

Show the policy and approval panel.

Click Approve.

### 8. Proof

Show:

```text
Transaction confirmed
Transaction verified
```

## Judge-Facing Proof Points

Make these visible:

```text
1. User supplied only a goal.
2. Plan was generated dynamically.
3. Tools were selected dynamically.
4. A tool failure triggered replanning.
5. Completion was independently verified.
6. Sensitive financial action required approval.
7. Policy enforcement remained deterministic.
8. The LLM never received a private key.
```

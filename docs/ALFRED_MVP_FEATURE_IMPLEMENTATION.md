# ALFRED --- MVP Product Surface & Feature Implementation Specification

## Purpose

Extend the existing ALFRED MVP so every visible navigation item and
button performs a real, useful action. Preserve the existing backend
architecture, API contracts, SSE execution, planning, replanning,
verification, finance approval flow, and demo-data integrations.

Do not add speculative enterprise features or fake functionality.

------------------------------------------------------------------------

## 1. Product Principle

ALFRED is an autonomous operations system.

The user should be able to:

1.  Understand what ALFRED does.
2.  Give ALFRED a natural-language goal.
3.  Watch it execute.
4.  Inspect the plan and actions.
5.  Review approvals.
6.  Inspect generated artifacts.
7.  Review task history and activity.
8.  Inspect knowledge/demo documents.
9.  Understand how ALFRED works.
10. Safely reset the demo/local environment.

Every displayed value must come from the backend, demo_data, actual task
state, or clearly labeled static product copy.

------------------------------------------------------------------------

## 2. Visual Direction --- Preserve It

The current visual language should remain:

-   dark
-   technical
-   restrained
-   retro-futuristic
-   terminal-inspired
-   mission-control/system-interface inspired
-   grid-based
-   angular
-   information-dense but organized

### Absolutely prohibited

Do not introduce:

-   purple, violet, lavender
-   electric blue or cyan
-   magenta
-   rainbow/colorful gradients
-   glassmorphism
-   excessive blur
-   glowing cards
-   giant rounded containers
-   gradient blobs
-   fake 3D objects
-   fake AI metrics
-   fake confidence percentages
-   meaningless charts
-   emoji as UI
-   excessive icons
-   excessive shadows
-   excessive animation

Use:

-   near-black
-   charcoal
-   warm white
-   muted gray
-   muted terminal green
-   restrained amber for warnings/attention

Green must remain muted rather than fluorescent.

------------------------------------------------------------------------

# 3. Sidebar Navigation

Make every existing sidebar destination functional:

-   Dashboard
-   Tasks
-   Approvals
-   Activity
-   Knowledge
-   Finance
-   Settings

Each item must route to a real page/view.

Do not leave dead navigation items.

If a feature cannot be meaningfully implemented within this MVP, remove
it rather than displaying "Not included in MVP."

------------------------------------------------------------------------

# 4. Dashboard

The dashboard is the main ALFRED control surface.

Include:

-   goal entry
-   suggested tasks
-   current agent state
-   recent tasks
-   pending approval summary
-   concise system health

### Goal Composer

Use:

`WHAT SHOULD ALFRED ACCOMPLISH TODAY?`

Input:

`> e.g. Prepare me for tomorrow's meeting with Rahul`

Action:

`> RUN`

Suggested operations:

-   PREPARE MEETING
-   HANDLE PENDING INVOICE
-   PROJECT UPDATE

Clicking a suggestion populates the input but does not execute
automatically.

### Recent Tasks

Use real task history.

Each row:

-   task number
-   goal
-   status
-   optional timestamp

Clicking a task opens its task detail/execution page.

Statuses:

-   RUNNING
-   COMPLETED
-   AWAITING APPROVAL
-   FAILED
-   REPLANNING

Do not invent tasks if no history exists.

------------------------------------------------------------------------

# 5. Tasks Page

Create:

`TASKS / 02`

Show a technical task list/table with:

-   ID
-   GOAL
-   STATUS
-   CREATED
-   RESULT

Clicking a task opens:

-   original goal
-   current status
-   plan
-   execution timeline
-   replanning events
-   verification
-   final result
-   generated artifacts

If persistent task history is not currently available, implement the
smallest compatible persistence needed. Do not introduce a new database
architecture.

------------------------------------------------------------------------

# 6. Approvals Page

Create:

`APPROVALS / 03`

Show pending consequential actions, primarily the finance invoice flow.

Each approval shows:

-   vendor
-   invoice
-   amount
-   policy result
-   state

Actions:

`> REVIEW`

`> APPROVE`

`> REJECT`

These must invoke the real backend endpoints.

### Empty State

`NO PENDING AUTHORIZATIONS`

`ALFRED has no consequential actions waiting for approval.`

------------------------------------------------------------------------

# 7. Approval Review

Clicking REVIEW opens a detailed approval view.

Display:

-   ACTION
-   VENDOR
-   AMOUNT
-   INVOICE
-   POLICY
-   CONTROL REQUIREMENT

Example:

`ACME SUPPLIES`

`₹3,800 INR`

`INV-1042`

`WITHIN POLICY`

`USER AUTHORIZATION REQUIRED`

Approve and Reject must call the backend.

After approval, show the real transaction and verification result.

After rejection, show rejection and ensure no transaction is executed.

------------------------------------------------------------------------

# 8. Activity / View Logs

Create:

`ACTIVITY / 04`

This is the system event-log interface.

Use actual backend/SSE events where available.

Example:

``` text
[20:41:02] GOAL_RECEIVED
           Prepare me for tomorrow's meeting

[20:41:03] PLAN_CREATED
           5 actions identified

[20:41:05] CALENDAR_SEARCH
           1 meeting found

[20:41:06] EMAIL_SEARCH
           4 relevant messages

[20:41:08] FILE_SEARCH
           No exact result

[20:41:09] REPLANNING
           Alternative search initiated

[20:41:11] FILE_SEARCH
           2 documents found

[20:41:14] DOCUMENT_CREATE
           meeting_brief.md

[20:41:16] VERIFICATION
           PASSED
```

Do not fabricate timestamps. If timestamps are unavailable, omit them.

The existing `VIEW LOGS` button should navigate here and, when
appropriate, focus the current task's events.

------------------------------------------------------------------------

# 9. Knowledge Page

Create:

`KNOWLEDGE / 05`

Expose documents already available through the existing
demo_data/backend integration.

Show:

-   filename
-   type/category
-   available action

Allow a lightweight document viewer:

-   filename
-   document content
-   close/back

Use actual backend/demo-data sources. Do not duplicate documents as
frontend assets.

------------------------------------------------------------------------

# 10. Finance Page

Create:

`FINANCE / 06`

Expose the existing finance/demo scenario.

For pending invoices show:

-   vendor
-   invoice ID
-   amount
-   policy status
-   payment status

Example:

``` text
ACME SUPPLIES
INV-1042
₹3,800
WITHIN POLICY
AWAITING APPROVAL
```

Clicking an invoice opens the approval flow.

After approval, show:

-   vendor
-   amount
-   transaction ID/hash if returned
-   policy result
-   approval result
-   verification result

Do not create real financial transactions. Clearly label simulated/demo
transaction identifiers when appropriate.

------------------------------------------------------------------------

# 11. Settings Page

Create:

`SETTINGS / 07`

Keep it small and useful.

### Connection

Show actual backend connectivity:

`CONNECTED`

or

`OFFLINE`

### Agent Components

Show actual availability where possible:

-   Planner
-   Executor
-   Replanner
-   Verifier
-   Policy Engine

### Demo Environment

Add:

`> RESET SYSTEM`

------------------------------------------------------------------------

# 12. Reset System

Implement the existing Reset System button.

When clicked, show confirmation:

``` text
RESET DEMO SYSTEM?

This clears the current local task/session state.

No external services will be affected.

[ CANCEL ]    [ RESET → ]
```

On confirmation:

-   clear frontend task state
-   clear cached task/event state
-   clear selected task
-   clear temporary approval state
-   return to a clean dashboard

If an existing backend demo-reset endpoint exists, use it.

If not, only add a minimal safe reset endpoint if actually necessary.

Never delete real user data or unrelated persistent data.

------------------------------------------------------------------------

# 13. See How It Works

Make the landing-page `SEE HOW IT WORKS` button functional.

Navigate/scroll to:

`HOW ALFRED WORKS`

Show:

### 01 --- GOAL

You describe the outcome you want.

### 02 --- PLAN

ALFRED determines the steps required.

### 03 --- ACT

It uses the available tools.

### 04 --- OBSERVE

It evaluates the results.

### 05 --- ADAPT

If an action fails or information is missing, ALFRED can replan.

### 06 --- VERIFY

ALFRED checks whether the intended outcome was achieved.

Use numbered stages, thin connecting lines, restrained green markers,
and subtle Motion transitions.

------------------------------------------------------------------------

# 14. Landing Page

Recommended structure:

## Hero

`GIVE ALFRED A GOAL.`

`LET IT HANDLE THE WORK.`

Buttons:

`LAUNCH ALFRED →`

`SEE HOW IT WORKS`

## Capability Strip

Only actual capabilities:

`PLANNER` `TOOL EXECUTION` `REPLANNING` `VERIFIER` `POLICY`

## How It Works

`GOAL → PLAN → ACT → OBSERVE → ADAPT → VERIFY`

## Example Task

Show a compact real-looking execution example using the existing demo
scenario. Do not invent backend results.

## Human Control

`AUTONOMOUS DOES NOT MEAN UNCONTROLLED.`

Explain:

-   approval gates
-   policy checks
-   verification
-   visible execution

## Final CTA

`GIVE ALFRED SOMETHING TO ACCOMPLISH.`

`LAUNCH ALFRED →`

------------------------------------------------------------------------

# 15. Landing Background

Use the established ALFRED kaleidoscopic computational tunnel.

It should use:

-   near-black background
-   very low-contrast grid
-   concentric geometry
-   radial technical lines
-   angular repeating structures
-   muted green/gray linework
-   central vanishing point

No purple, blue, cyan, neon, or gradients.

The tunnel must never interfere with readability.

Suggested visibility:

-   Landing: visible
-   Dashboard: subtle
-   Task execution: barely visible
-   Approval: no distracting background
-   Result: subtle

------------------------------------------------------------------------

# 16. Task Detail Page

Create:

`TASK / 001`

Display the goal and current status.

Main layout:

### LEFT --- PLAN

1.  Find meeting
2.  Gather communication
3.  Find project information
4.  Create briefing
5.  Verify result

### CENTER --- EXECUTION

Live backend events/SSE.

### RIGHT --- RESULT / CONTROL

Show:

-   current status
-   approvals
-   artifacts
-   verification

Do not overload the page.

------------------------------------------------------------------------

# 17. Artifact Viewer

Generated artifacts such as:

`meeting_brief.md`

must be clickable.

Open a lightweight viewer showing:

-   filename
-   generated content
-   verification status
-   close/back

Use backend-provided artifact content.

------------------------------------------------------------------------

# 18. Agent Status

Do not display a fake `100%` readiness number.

Prefer:

``` text
AGENT STATUS

■ READY

PLANNER        OK
EXECUTOR       OK
REPLANNER      OK
VERIFIER       OK
POLICY         OK
```

If unavailable:

`OFFLINE`

If unknown:

`UNKNOWN`

Never fabricate percentages.

------------------------------------------------------------------------

# 19. Error States

Handle:

-   backend offline
-   task not found
-   SSE disconnected
-   failed task
-   failed tool
-   rejected approval
-   verification failure
-   invalid task request

Example:

``` text
SYSTEM CONNECTION LOST

ALFRED cannot reach the execution service.

[ RETRY ]
```

Do not hide errors.

------------------------------------------------------------------------

# 20. Motion Requirements

Use Framer Motion / Motion for React for meaningful transitions:

-   page transitions
-   hero reveal
-   section reveal
-   task state changes
-   live event entry
-   replanning event appearance
-   approval entrance
-   result reveal
-   navigation transitions

Avoid:

-   bounce
-   excessive spring physics
-   constant pulsing
-   animated gradients
-   fake "AI thinking"
-   confetti
-   particle explosions
-   excessive parallax

Respect `prefers-reduced-motion`.

------------------------------------------------------------------------

# 21. Backend Integration Rules

Continue using the existing API contracts.

Centralize API calls in the existing service layer.

Never expose in frontend:

-   OpenAI secret keys
-   Supabase service-role keys
-   private keys
-   blockchain secrets
-   backend credentials

Use:

`VITE_API_URL`

for the frontend API base URL.

Do not create a second API architecture.

------------------------------------------------------------------------

# 22. No Fake Functionality

Do not implement buttons that merely:

-   show "Coming soon"
-   display fake dialogs
-   change local state without backend effect
-   show static fake data
-   simulate backend responses

If a visible feature exists, it must work.

If it cannot be implemented safely in this MVP, remove it.

------------------------------------------------------------------------

# 23. Implementation Priority

## P0

-   Sidebar routing
-   Dashboard
-   Tasks page
-   Task detail
-   Approvals
-   Approval actions

## P1

-   Activity/logs
-   Knowledge viewer
-   Finance page
-   Reset System
-   See How It Works

## P2

-   Artifact viewer
-   Landing sections
-   Connection status
-   Motion polish

## P3

-   Responsive refinement
-   Accessibility
-   Empty/error states
-   final visual QA

------------------------------------------------------------------------

# 24. Acceptance Criteria

### Landing

-   [ ] Hero is polished
-   [ ] Launch ALFRED works
-   [ ] See How It Works works
-   [ ] How It Works section exists
-   [ ] Tunnel background is visible but restrained

### Dashboard

-   [ ] Goal submission works
-   [ ] Suggested goals work
-   [ ] Recent tasks work
-   [ ] Agent status is meaningful
-   [ ] No fake metrics

### Tasks

-   [ ] Task list works
-   [ ] Task selection works
-   [ ] Task details work
-   [ ] Real execution data is shown

### Approvals

-   [ ] Pending approvals display
-   [ ] Review works
-   [ ] Approve works
-   [ ] Reject works
-   [ ] State comes from backend

### Activity

-   [ ] Real events are visible
-   [ ] Logs are readable
-   [ ] View Logs works

### Knowledge

-   [ ] Real demo documents are listed
-   [ ] Document viewer works

### Finance

-   [ ] Pending invoice is visible
-   [ ] Policy status is visible
-   [ ] Approval flow works
-   [ ] Transaction result is visible
-   [ ] Verification result is visible

### Settings

-   [ ] Backend status is shown
-   [ ] Agent component status is shown
-   [ ] Reset System works safely

### Execution

-   [ ] SSE works
-   [ ] Replanning is visible
-   [ ] Verification is visible
-   [ ] Completion is visible
-   [ ] Failure is handled

------------------------------------------------------------------------

# 25. Final QA

Test at:

-   1280 × 720
-   1440 × 900
-   1920 × 1080
-   mobile width

Check:

-   no horizontal overflow
-   no clipped text
-   no overlapping content
-   no dead buttons
-   no dead navigation
-   no fake metrics
-   no console errors
-   no API errors
-   no duplicated SSE events
-   no visual regressions

------------------------------------------------------------------------

# 26. Final Creative Direction

ALFRED should feel like:

**a window into an autonomous computer system.**

Not:

-   a chatbot
-   a generic SaaS dashboard
-   a purple AI landing page
-   a cyberpunk game interface
-   a collection of cards

The product should communicate:

``` text
GOAL
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
OUTCOME
```

Prefer:

**clarity over decoration**\
**function over spectacle**\
**information over empty visual polish**\
**restraint over effects**

------------------------------------------------------------------------

# 27. Deliverables

After implementation, report:

1.  Files changed.
2.  Routes/pages added.
3.  API endpoints used.
4.  Any backend endpoints added.
5.  Features completed.
6.  Features intentionally excluded.
7.  Test results.
8.  Build result.
9.  Remaining issues.

Do not claim completion until the actual flows have been tested
end-to-end.

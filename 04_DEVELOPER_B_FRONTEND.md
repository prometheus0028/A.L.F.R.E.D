# Developer B — Frontend / UX Implementation

## Mission

Build the ALFRED frontend inside the existing `frontend/` directory.

You own:

```text
frontend/
```

You do NOT own:

```text
backend/
demo_data/
requirements.txt
```

Never edit those areas.

## First Rule: Do Not Vibe-Code the UI

This is a strict requirement.

The frontend must look like a serious autonomous-agent product designed by a professional product designer.

Do NOT create:

- giant gradient backgrounds
- neon cyan/purple AI aesthetics
- glassmorphism
- excessive translucent cards
- floating glowing blobs
- decorative 3D cubes
- random illustrations
- oversized rounded containers everywhere
- excessive drop shadows
- fake dashboard metrics
- meaningless charts
- fake activity numbers
- decorative icons replacing labels
- emoji as UI
- excessive animations
- animated gradients
- typewriter effects
- bouncing buttons
- constant pulsing
- "AI magic" visual effects
- excessive pill-shaped UI
- unnecessary modals
- dense card grids
- visual elements with no semantic purpose

Do not copy generic "AI dashboard" templates.

The product should feel closer to a high-quality enterprise operations interface than a futuristic AI landing page.

## Visual Philosophy

Use:

```text
clear hierarchy
restrained color
strong typography
generous whitespace
consistent alignment
subtle borders
minimal shadows
purposeful states
```

Every element must communicate something.

If removing a visual element does not reduce usability, remove it.

## Avoid Frontend Hallucination

Do not invent:

- fake agent metrics
- fake integrations
- fake user counts
- fake transaction volume
- fake system health statistics
- fake charts
- fake notifications
- fake "AI confidence" percentages

Only show data that comes from the backend or is explicitly marked as demo data.

## Existing Frontend

Inspect:

```text
frontend/src/
```

before making changes.

Do not blindly delete the existing application.

Reuse useful existing components and styles where appropriate.

However, if existing UI elements are clearly vibecoded, generic, decorative, or inconsistent with the ALFRED product, refactor or remove them.

Do not preserve bad UI merely because it already exists.

## Primary UI

Build one strong workspace rather than many unnecessary pages.

Recommended structure:

```text
┌──────────────────────────────────────────────────────┐
│ ALFRED                                  Agent Ready  │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Goal                                                 │
│ ┌──────────────────────────────────────────────────┐ │
│ │ What should ALFRED accomplish?                  │ │
│ └──────────────────────────────────────────────────┘ │
│                                    [Run task]         │
│                                                      │
├──────────────────────┬───────────────────────────────┤
│ PLAN                 │ EXECUTION                    │
│                      │                               │
│ 1 Find meeting       │ ✓ Goal understood             │
│ 2 Search email       │ ✓ Plan created                │
│ 3 Search files       │ ✓ Calendar searched           │
│ 4 Create briefing    │ ● Searching email             │
│ 5 Verify             │ ○ Verification                │
│                      │                               │
└──────────────────────┴───────────────────────────────┘
```

Exact visual implementation is up to you, but maintain restraint.

## Core Components

Use a small component system.

Suggested:

```text
frontend/src/
├── components/
│   ├── GoalInput
│   ├── TaskHeader
│   ├── PlanView
│   ├── ExecutionTimeline
│   ├── ApprovalPanel
│   ├── ResultPanel
│   └── StatusIndicator
├── services/
│   ├── api
│   └── mockApi
├── hooks/
│   └── taskEvents
├── pages/
│   └── Workspace
└── ...
```

Adapt to the existing source structure rather than creating duplicate architecture.

## Mock-First Development

You must be able to build and test without Developer A's backend.

Create a mock API with the same interface as the real API.

Required functions:

```text
createTask()
getTask()
approveAction()
rejectAction()
subscribeToTaskEvents()
```

The mock should simulate:

```text
goal_received
plan_created
tool_started
tool_completed
replanning
approval_required
task_completed
```

Include a deterministic demo sequence.

At integration time, switch the implementation to the real API without changing UI components.

## API Boundary

Implement against:

`02_SHARED_CONTRACTS.md`

Do not invent alternate field names.

Use:

```text
task_id
status
current_step
total_steps
plan
actions
approval
result
```

## Execution Timeline

This is a major product surface.

It should clearly show:

```text
completed
running
pending
failed
replanned
```

Example:

```text
✓ Goal understood
✓ Plan created
✓ Calendar searched
✓ Meeting found
✓ Email searched
↻ Replanning
✓ Project status found
● Creating briefing
○ Verification
```

The timeline should be readable without animation.

Animation is optional and must never be necessary to understand state.

## Replanning State

Make recovery visually distinct but restrained.

Example:

```text
Replanning

No exact document was found.
ALFRED is trying an alternative search.
```

Then show the successful recovery.

Do not use dramatic red screens or flashing warnings.

## Approval UI

For finance:

```text
Payment requires approval

Acme Supplies
₹3,800 INR
Invoice INV-1042

Policy
Vendor approved
Within ₹5,000 limit

[Reject] [Approve]
```

The approval interface should make the consequence obvious.

Do not hide important information.

Do not use green/red purely as decoration.

## Result UI

Meeting:

```text
Task complete

Meeting briefing created and verified.

Sources
1 calendar event
4 emails
2 documents

Created
meeting_brief.md
```

Finance:

```text
Payment verified

Acme Supplies
₹3,800 INR

Policy passed
User approved
Transaction confirmed

0xDEMO...
```

## Responsive Design

At minimum:

- desktop-first
- reasonable laptop widths
- no horizontal overflow
- no clipped text
- no overlapping panels

Keep the UI usable at approximately 1280×720.

## Typography

Use the existing project typography if already established.

Do not introduce multiple unrelated fonts.

Minimum readable body size should generally be around 14–16px for the web UI, with strong hierarchy for headings.

Do not make everything huge.

## Color

Use a restrained palette.

Recommended principles:

```text
1 primary surface
1 secondary surface
1 text hierarchy
1 accent
semantic success/warning/error colors
```

Do not turn every state into a different bright color.

## Motion

Use little or no motion.

Acceptable:

- subtle state transition
- short opacity transition
- progress transition

Not acceptable:

- bouncing cards
- floating objects
- constant pulsing
- animated gradients
- excessive entrance animations
- decorative parallax

## Icons

Use icons only when they improve comprehension.

Never use icons as decoration.

Do not introduce a giant icon library solely for visual density.

## Testing

Test:

```text
goal submission
loading state
mock event stream
plan rendering
execution timeline
replanning rendering
approval rendering
approve action
reject action
completion rendering
failure rendering
empty states
long goal text
long tool summary
```

## Definition of Done

The frontend is done when:

1. it runs independently using mock data
2. a user can submit a natural-language goal
3. the UI visibly shows planning and execution
4. the UI shows tool progress
5. the UI shows replanning
6. the approval interface works
7. the final result is clear
8. the UI has no overlap or overflow
9. the UI contains no vibecoded decorative elements
10. switching from mock API to real API requires minimal change

## Final Visual QA

Before committing:

- inspect every screen manually
- check 1280×720
- check for overflow
- check for inconsistent spacing
- remove redundant cards
- remove fake data
- remove unnecessary decoration
- verify all buttons have meaningful actions
- verify every status has a readable state

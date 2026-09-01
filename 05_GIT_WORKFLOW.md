# Git Workflow — Two Developers, Zero Overlap

## Goal

Both developers work simultaneously and merge into `main` with minimal conflict.

## Branches

Use:

```text
main
dev/backend-agent
dev/frontend-ui
```

Developer A:

```text
dev/backend-agent
```

Developer B:

```text
dev/frontend-ui
```

## Ownership

Developer A changes only:

```text
backend/
demo_data/
requirements.txt
```

Developer B changes only:

```text
frontend/
```

This path ownership is the primary conflict-prevention mechanism.

## Initial Setup

One developer should verify the existing repository structure before parallel implementation.

Do not create competing root configurations.

If a root-level setup change is required, Developer A owns `requirements.txt` and backend-side root configuration.

Developer B owns frontend configuration inside `frontend/`.

## Commit Rules

Use focused commits.

Developer A examples:

```text
feat(agent): implement dynamic planner
feat(agent): add execution loop
feat(tools): implement demo data tools
feat(agent): add replanning
feat(agent): add verification
feat(finance): add policy engine
feat(blockchain): add transaction adapter
```

Developer B examples:

```text
feat(ui): build goal workspace
feat(ui): add execution timeline
feat(ui): add mock task service
feat(ui): add approval panel
feat(ui): add result view
refactor(ui): remove decorative dashboard elements
```

Avoid:

```text
updates
changes
final
stuff
fix
misc
```

## Commit Scope

Before committing:

```bash
git status
git diff --stat
git diff
```

Confirm you touched only your owned paths.

Developer A should never see:

```text
frontend/...
```

in their commit.

Developer B should never see:

```text
backend/...
demo_data/...
requirements.txt
```

in their commit.

## Pulling Changes

Because source ownership does not overlap, neither developer needs to repeatedly merge the other's work during implementation.

Do not perform unnecessary rebases just to stay busy.

Focus on your owned boundary.

## Contract Changes

If a contract must change:

1. stop implementation
2. document the proposed change
3. update the shared contract document
4. notify the other developer
5. ensure both sides remain compatible

Do not silently change API fields.

## Merge Order

Recommended:

```text
main
 ↓
merge dev/backend-agent
 ↓
backend smoke test
 ↓
merge dev/frontend-ui
 ↓
configure frontend to real API
 ↓
integration smoke test
```

Why backend first?

The backend establishes the live service against which the frontend adapter is tested.

The frontend can already be fully developed against its mock API.

## Final Integration Owner

Developer A owns backend/root integration configuration.

Developer B owns frontend-side API configuration inside `frontend/`.

Neither developer should rewrite the other's implementation.

## If a Conflict Occurs

Do not blindly choose "ours" or "theirs."

First identify:

```text
Which developer owns this file?
```

Then:

- preserve the file owner's implementation
- move any necessary change through the correct owner
- avoid resolving by copying entire directories

A conflict should be unusual because the ownership boundaries are intentionally separate.

## Final Main Branch Checks

After both branches are merged:

```bash
git status
```

Then:

```bash
# backend
python -m pytest
```

and:

```bash
# frontend
npm install
npm run build
```

Then manually run the complete application.

## Do Not Commit

Never commit:

```text
.env
.env.local
node_modules/
dist/
__pycache__/
*.pyc
.venv/
secrets
private keys
API keys
```

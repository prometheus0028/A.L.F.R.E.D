# ALFRED Frontend — Anti-Vibecoding Design Standard

## This document is mandatory for Developer B

The ALFRED frontend must not look AI-generated in the negative sense of the term.

The goal is a restrained, professional operations workspace.

## Product Character

ALFRED should feel:

```text
precise
calm
technical
trustworthy
functional
enterprise-ready
```

It should not feel:

```text
flashy
gaming-like
cyberpunk
NFT-like
template-generated
"AI magic"
```

## Layout Rules

Use a consistent layout grid.

Recommended:

```text
top navigation/header
main workspace
execution area
result/approval area
```

Avoid filling every empty area.

Whitespace is intentional.

## Card Rules

Cards are allowed when they group meaningful information.

Good:

```text
Execution
12 actions
1 replan
Verified
```

if those values are real.

Bad:

```text
AI POWER
98.4%
AGENT IQ
12.4K ACTIONS
```

when these are fabricated.

Do not create a card simply because the layout has empty space.

## Background Rules

Prefer:

```text
solid background
subtle surface separation
fine borders
```

Avoid:

```text
gradient mesh
glowing circles
floating blobs
grid overlays
particle backgrounds
large decorative shapes
```

## Color Rules

Use color semantically.

For example:

```text
neutral = normal
accent = active
success = verified
warning = approval/recovery
error = failed
```

Do not make the entire interface neon.

Do not use five accent colors.

## Border Radius

Use moderate, consistent rounding.

Avoid:

```text
everything = giant pill
```

Buttons should look like buttons.

Inputs should look like inputs.

Panels should look like panels.

## Shadows

Use subtle elevation only where necessary.

Avoid:

```text
heavy black shadows
glowing shadows
multiple layered shadows
```

## Typography

Use one coherent type family.

Hierarchy should be clear:

```text
page title
section title
body
metadata
```

Do not make every heading oversized.

Avoid all-caps paragraphs.

## Icons

Icons are functional.

Good uses:

```text
status indicator
expand/collapse
navigation
copy
external result
```

Bad uses:

```text
random icons beside every sentence
giant decorative AI icon
emoji
```

## Animation

Use animation only to communicate state changes.

Allowed:

```text
150–250ms opacity/position transitions
subtle progress changes
```

Avoid:

```text
bounce
shake
spin
pulse loops
typewriter
parallax
auto-playing effects
```

The product must still make sense with animations disabled.

## Execution Timeline

This is the main visual storytelling mechanism.

Use hierarchy:

```text
completed
current
pending
recovered
```

A user should understand the entire execution in a few seconds.

## Approval Panel

The approval UI must emphasize:

```text
WHAT
HOW MUCH
WHY
POLICY
WHAT WILL HAPPEN NEXT
```

Never hide consequential information behind tiny text.

## Empty States

Do not use decorative illustrations.

Example:

```text
No active task

Enter a goal above to start ALFRED.
```

## Loading States

Use simple skeletons or text states.

Example:

```text
Planning task…
```

Do not create fake AI animations.

## Error States

Be direct.

Good:

```text
Could not find a matching project document.

ALFRED is attempting an alternative search.
```

Bad:

```text
Oops! The AI magic hit a turbulence field.
```

## Content Density

Prefer fewer high-value elements.

The frontend should NOT become a wall of:

- cards
- badges
- pills
- charts
- metrics
- decorative labels

## Anti-Pattern Checklist

Remove anything resembling:

```text
[ ] gradient blobs
[ ] glowing borders
[ ] neon text
[ ] glass cards
[ ] fake statistics
[ ] unnecessary charts
[ ] emoji
[ ] excessive icons
[ ] animated background
[ ] decorative 3D objects
[ ] huge rounded cards
[ ] excessive shadows
[ ] meaningless badges
[ ] fake "AI confidence"
[ ] fake integrations
```

## Final Test

Ask:

> If I remove this element, does the user lose information, navigation, feedback, or control?

If the answer is no, remove it.

The strongest ALFRED frontend should look almost obvious in hindsight: clean, focused, and built around the autonomous execution state.

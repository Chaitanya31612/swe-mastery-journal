# 05 - UI/UX Craft And Product Thinking

UI/UX is subjective at the edges. The fundamentals are not.

Good interface work is mostly:

```text
clear hierarchy
predictable interaction
stable layout
fast feedback
useful defaults
recoverable mistakes
low cognitive load
accessible semantics
polished states
```

---

## The Core Idea

Users do not experience your component tree.

They experience:

```text
Where am I?
What can I do?
What just happened?
What should I do next?
Can I recover if this goes wrong?
```

Every screen should answer those questions quickly.

Senior intuition: UI is communication before decoration.

---

## Visual Hierarchy

Hierarchy tells the eye what matters.

Tools:

- size
- weight
- color
- contrast
- spacing
- grouping
- alignment
- position
- motion
- copy

Bad hierarchy:

```text
title, metadata, button, warning, table header, and footer all have equal visual weight
```

Better hierarchy:

```text
primary page purpose
  strongest

supporting details
  quieter

primary action
  visible but not screaming

secondary actions
  available but lower emphasis

danger actions
  isolated and explicit
```

Practical trick:

```text
Squint at the screen.
If everything is equally loud, nothing has hierarchy.
```

---

## Spacing Is Meaning

Spacing is not empty decoration. It communicates relationship.

```text
tight spacing
  these things belong together

large spacing
  this is a new group or section
```

Bad:

```text
label far from input
input close to next label
```

The eye may associate the input with the wrong label.

Better:

```text
label
small gap
input
larger gap
next label
```

Use a spacing scale:

```text
4, 8, 12, 16, 24, 32, 48, 64
```

Senior intuition: inconsistent spacing makes users spend brain cycles grouping the page.

---

## Alignment

Alignment creates calm.

Good interfaces usually have fewer invisible lines:

```text
left edge of title
left edge of content
left edge of form fields
left edge of table
```

Bad:

```text
buttons float slightly off
labels have random widths
cards have inconsistent padding
icons are not optically centered
```

Practical trick:

```text
Draw vertical lines over the UI.
If every element starts somewhere different without reason, the screen will feel amateur.
```

---

## Typography

Typography controls rhythm and confidence.

Useful defaults:

```text
body
  readable size, comfortable line height

heading
  clear contrast from body, not too many sizes

metadata
  smaller or quieter, not both to unreadability

buttons
  action-oriented verb
```

Bad:

```text
Welcome to the user management dashboard where you can manage users.
```

Better:

```text
Users
Manage access, roles, and invitations.
```

Senior rule: copy is part of interface design. Good copy reduces UI complexity.

---

## Color

Color should not be the only carrier of meaning.

Bad:

```text
red border only means error
```

Better:

```text
red border
error icon
error text
aria-invalid
described-by relationship
```

Use color roles:

```text
surface
text
muted text
border
primary
success
warning
danger
focus
```

Avoid one-off colors unless the product has a real reason.

Senior intuition: consistent color roles create trust faster than beautiful random palettes.

---

## Interaction States

Every interactive element needs states.

```text
default
hover
active
focus
disabled
loading
success
error
selected
pressed
expanded
```

Bad button:

```text
click Save
button stays identical
request runs
maybe something happens
```

Better:

```text
click Save
button becomes Saving...
duplicate submit blocked
nearby status updates
success or error is shown
focus remains predictable
```

Senior rule: no action should feel like shouting into the void.

---

## Loading States

Loading states should preserve context.

Bad:

```text
replace entire screen with spinner
```

Better:

```text
keep layout shell
show skeleton where content will appear
preserve already-known content
show progress near the affected region
```

Choose loading pattern:

```text
spinner
  unknown wait, small region, short action

skeleton
  content layout is predictable

progress bar
  measurable progress

optimistic UI
  action is likely to succeed and reversible

disabled plus label change
  form submission or irreversible in-flight action
```

Interesting fact: skeletons can feel slower than spinners when used for tiny waits because they add visual noise. Do not skeleton everything.

---

## Empty States

An empty state is not a blank component.

It should answer:

```text
What is this area?
Why is it empty?
What can I do next?
```

Bad:

```text
No data.
```

Better:

```text
No projects yet
Create your first project to start tracking work.
[Create project]
```

Types:

```text
first-use empty
  educate and invite action

filtered empty
  explain filter mismatch and offer reset

permission empty
  explain access limitation and next step

error empty
  explain failure and recovery
```

Senior intuition: empty states are onboarding moments.

---

## Error States

Error UX needs three things:

```text
what happened
what it means
what the user can do
```

Bad:

```text
Something went wrong.
```

Better:

```text
We could not save your changes.
Your edits are still here. Check your connection and try again.
[Try again]
```

For field errors:

```text
place error near field
use specific language
preserve entered value
move focus only when helpful
```

For page errors:

```text
preserve navigation
show retry
include support code only if useful
avoid dead ends
```

Senior rule: the user should never lose work because our system got confused.

---

## Latency Masking

Big tech products often feel smooth because they hide latency intelligently.

Patterns:

```text
instant acknowledgement
  change button text immediately

optimistic update
  show likely result before server confirms

prefetch
  load probable next route or data

progressive reveal
  show ready parts first

stale-while-revalidate
  show cached data, refresh quietly

transition priority
  keep input responsive while expensive UI updates later

undo instead of confirm
  execute low-risk action immediately, allow recovery
```

Example:

```text
Gmail archive
  email disappears immediately
  snackbar offers Undo
  user does not wait for a confirmation dialog
```

Trade-off:

```text
undo works well for reversible actions
confirm works better for high-risk irreversible actions
```

Senior intuition: seamless UX is often not faster servers. It is better sequencing.

---

## Progressive Disclosure

Do not show all power at once.

```text
default path
  obvious and simple

advanced options
  available when needed

dangerous actions
  separated and explicit
```

Bad:

```text
New user sees 18 fields, 7 toggles, 3 advanced panels
```

Better:

```text
show required basics
hide advanced defaults behind "Advanced settings"
explain consequences near risky controls
```

Senior rule: powerful does not mean visually busy.

---

## Affordance And Signifiers

Affordance:

```text
what an object can do
```

Signifier:

```text
the clue that tells the user what it can do
```

Example:

```text
card is clickable
```

Need signifiers:

- cursor
- hover state
- focus state
- maybe chevron
- clear title
- link semantics if navigation

Bad:

```text
entire card is clickable but nothing visually indicates it
```

Senior intuition: hidden affordances create "expert-only" UI.

---

## Accessibility As UX Foundation

Accessibility is not charity work added later. It is robust interface engineering.

Core practices:

- use semantic HTML first
- buttons perform actions
- links navigate
- labels connect to inputs
- focus is visible
- keyboard paths work
- errors are announced or associated
- color is not the only signal
- motion respects user preference
- modal focus is trapped and restored

Bad:

```html
<div onclick="save()">Save</div>
```

Better:

```html
<button type="button">Save</button>
```

Senior rule: if you fight the browser's native semantics, you inherit all the behavior you broke.

---

## Motion

Motion should explain change.

Good motion:

- shows where something came from
- confirms an action
- guides attention
- makes state changes legible
- stays short

Bad motion:

- delays common work
- moves too much
- hides content
- ignores reduced motion
- exists only to show off

Useful timing:

```text
100-150ms
  tiny hover or tap feedback

150-250ms
  small transitions

250-400ms
  larger panels or route-level movement
```

Senior intuition: motion is punctuation, not the paragraph.

---

## Microcopy

Microcopy reduces uncertainty.

Bad:

```text
Submit
```

Better:

```text
Create project
Invite teammate
Save changes
```

Bad:

```text
Invalid input
```

Better:

```text
Password must be at least 12 characters.
```

Good microcopy:

- uses user language
- says what happens
- avoids blame
- is specific
- appears where needed
- does not over-explain obvious things

Senior intuition: vague copy makes users build their own mental model, often incorrectly.

---

## Information Scent

Users follow clues.

Strong scent:

```text
Settings -> Billing -> Update payment method
```

Weak scent:

```text
Manage -> Advanced -> Other -> Card
```

Improve scent with:

- descriptive labels
- predictable grouping
- breadcrumbs when hierarchy is deep
- page titles that match navigation labels
- action names that match user intent

Senior rule: users should not need memory when recognition can do the job.

---

## Taste Builders

To improve taste, do reps deliberately:

1. Screenshot a polished product screen.
2. Redraw the layout with boxes only.
3. Mark spacing scale, hierarchy, and alignment.
4. List every state the UI supports.
5. Rewrite the copy in plain language.
6. Ask what happens when data is empty, slow, failed, long, or unauthorized.

This trains the part of your brain that sees structure under beauty.

---

## UI Review Checklist

Use this before shipping:

- Is the primary action obvious?
- Is the secondary action less loud?
- Are destructive actions isolated?
- Does spacing show grouping?
- Are labels close to controls?
- Does loading preserve context?
- Is empty state useful?
- Does error state help recovery?
- Is focus visible and logical?
- Can keyboard users complete the flow?
- Does the URL match user expectations?
- Does the page avoid unexpected layout shifts?
- Does the UI acknowledge actions immediately?
- Is copy specific and human?

---

## The One-Sentence Model

Great UI/UX makes system state, available action, and next step obvious while protecting the user from latency, mistakes, and cognitive noise.

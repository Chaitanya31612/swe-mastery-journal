## Follow a concrete example

```text
Question: Can a new agent hand off overdue tickets correctly?
Task: “Your shift is ending. Move these eligible tickets to Team B.”
Observe: correct selection, audience understanding, partial-failure recovery.
Success metric: correct assignments / eligible handoff attempts.
Guardrail: wrong-team assignments and lost drafts.
```
Use synthetic tasks and minimal event data. Write the event definition before installing an analytics SDK.
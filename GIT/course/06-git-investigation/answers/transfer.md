# One valid adaptation

Create a separate clean checkout at the relevant commit or a new temporary branch, run tests there, and leave the active working tree intact.

Inspect and remove the temporary worktree with Git after preserving any needed output. Do not accidentally run cleanup in the primary checkout.

**Explain back:** Make the symptom repeatable, then search history. What changed in the new condition?

What would make your answer fail?
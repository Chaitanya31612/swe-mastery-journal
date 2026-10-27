## Trace the execution

Draw the dependency graph. Loading a ticket and a member directory can overlap.

Loading comments using an ID returned by a creation request cannot begin before that ID exists.

For a stale search: A starts, B starts, B succeeds, A fails. The final UI should show B and no stale error.

Use controlled promises to reproduce this exact order. Avoid a fixed sleep as proof.
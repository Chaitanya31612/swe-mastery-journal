## Understand the idea

Cherry-pick applies a commit’s change onto the current base and usually creates a new commit. It does not bring every dependency of that change automatically. A patch that applies cleanly can still call a helper absent on the release branch.

Revert creates a new corrective commit. It is often easier for collaborators than rewriting a published branch. Reverting a merge requires choosing the intended mainline parent and understanding future merge consequences; do not guess from parent numbers.

Before any history operation, inspect the graph, outgoing patch, and current work. Use a disposable worktree for a release rehearsal. Record which release line received the fix and how it was tested there.

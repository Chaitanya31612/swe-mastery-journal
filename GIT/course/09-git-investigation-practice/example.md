## Follow a concrete example

```sh
git reflog -10
git show <candidate-id> --stat
git branch rescue/investigation <candidate-id>
git worktree add --detach ../ticket-investigation <candidate-id>
# Run the repeatable test there, then inspect its result.
git worktree list
```

Use a fresh scratch location. A detached worktree is suitable for inspection; create a deliberate branch if you intend to keep new commits.

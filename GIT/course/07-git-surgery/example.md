## Follow a concrete example

```sh
git show <fix-id> --stat
git show <fix-id>
# In a clean, deliberate release-fix branch/worktree:
git cherry-pick <fix-id>
# On conflict, inspect intent, then continue or abort:
git cherry-pick --abort
```
Replace placeholders with inspected IDs. Do not execute these commands in an unrelated active checkout.
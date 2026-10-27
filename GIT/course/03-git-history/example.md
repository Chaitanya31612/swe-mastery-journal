# A small example

```sh
git log --oneline --graph --decorate --all -12
git diff main...HEAD       # branch changes since merge base
# In a disposable branch only:
git rebase main
# If a conflict occurs: inspect, edit, stage, then
git rebase --continue
# Or return to the pre-rebase state:
git rebase --abort
```
Create two branches editing one sentence differently. Write the intended final behavior before resolving the conflict.
# A small example

```sh
git status --short
git reflog -8
# Inspect a candidate before recovering it.
git show <old-commit-id> --stat
# Create a new name; do not overwrite current work to inspect it.
git branch rescue/old-tip <old-commit-id>
# For an already published bad commit, on a suitable repair branch:
git revert <bad-commit-id>
```
Use actual IDs discovered in the disposable lab. Angle-bracket placeholders are not literal shell arguments.
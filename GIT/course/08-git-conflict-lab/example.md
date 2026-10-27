## Follow a concrete example

```sh
git status
git diff
git show :1:path/to/file  # common base, when present in an unmerged index
git show :2:path/to/file  # one side
git show :3:path/to/file  # other side
```

In a scratch repository, make one branch add authorization and another refactor the method. The final code must preserve both the new structure and the permission rule.

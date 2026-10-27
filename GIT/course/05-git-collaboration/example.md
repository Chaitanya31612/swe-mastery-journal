# A small example

```sh
git fetch origin
git log --oneline HEAD..origin/main
git diff --stat HEAD...origin/main
# When you deliberately want only a fast-forward update:
git pull --ff-only
git branch -vv
```

In the lab, use a local bare repository as a fake remote. Make another clone and push a commit from there. Observe that your working branch does not move on fetch.

# A small example

```sh
# Run only inside the supplied disposable Git lab.
git status --short
git diff                 # working tree versus index
git diff --cached        # index versus HEAD
git log --oneline --graph --decorate -8
git show HEAD:notes.txt
```

Write A in notes.txt and stage it. Change the file to B without staging again. Predict the next commit content before opening either diff.

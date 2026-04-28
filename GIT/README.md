# Git Mastery Journal

> Goal: build senior-level Git judgment, not just command memory.
> Use this as a revision guide, a debugging manual, and a lab book.

---

## How To Use This Folder

Read the docs in order once. After that, jump by situation:

- "I changed files and want to understand what Git sees" -> `docs/01-local-workflow-index-and-diff.md`
- "I need to design history cleanly" -> `docs/02-history-branches-merge-and-rebase.md`
- "I messed something up" -> `docs/03-undo-recovery-and-reflog.md`
- "Remote branches are confusing" -> `docs/04-remotes-collaboration-and-prs.md`
- "I need senior-level debugging tools" -> `docs/05-archaeology-bisect-worktree-and-advanced-tools.md`
- "I want reps" -> `exercises/01-practice-labs.md`
- "I want checked solutions" -> `exercises/01-practice-labs-answers.md`

---

## Folder Structure

```text
GIT/
├── README.md
├── docs/
│   ├── 00-mental-model-and-internals.md
│   ├── 01-local-workflow-index-and-diff.md
│   ├── 02-history-branches-merge-and-rebase.md
│   ├── 03-undo-recovery-and-reflog.md
│   ├── 04-remotes-collaboration-and-prs.md
│   └── 05-archaeology-bisect-worktree-and-advanced-tools.md
└── exercises/
    ├── 01-practice-labs.md
    └── 01-practice-labs-answers.md
```

---

## The Senior Git Mental Model

Most Git confusion comes from treating Git as "a folder with versions".

That is too weak.

Git is closer to this:

```text
working tree  -> files you can edit
index         -> proposed next commit
object store  -> immutable content database
refs          -> movable names pointing at commits
reflog        -> local safety trail of ref movements
remotes       -> other object stores you exchange commits with
```

When you know which layer a command touches, the command becomes predictable.

---

## Command Decision Map

Use this when you know the situation but not the command.

```text
Need to inspect?
  status        -> what changed at each layer
  diff          -> working tree vs index
  diff --cached -> index vs HEAD
  log           -> commit graph
  show          -> one object or commit

Need to stage?
  add           -> copy working tree content into the index
  restore       -> copy content from a source into working tree or index

Need to make history?
  commit        -> write index as a new commit
  branch        -> create or move a ref
  switch        -> move HEAD and update files

Need to integrate?
  merge         -> preserve branch topology
  rebase        -> replay commits onto a new base
  cherry-pick   -> replay selected commits

Need to undo?
  restore       -> undo file-level changes
  reset         -> move branch and optionally index/working tree
  revert        -> create an inverse commit
  reflog        -> find where refs used to point

Need remote work?
  fetch         -> download objects and update remote-tracking refs
  pull          -> fetch plus merge/rebase
  push          -> upload commits and update a remote ref
```

---

## Senior Rules Of Thumb

- Inspect before changing history: `git status`, `git log --oneline --graph --decorate --all`, `git diff`, `git diff --cached`.
- Prefer `fetch` then inspect over blind `pull` when the branch matters.
- Use `rebase` to clean your private branch. Use `merge` when preserving branch topology matters.
- Never rewrite public history unless the team agreed to it and you know exactly who is affected.
- `revert` is the default public undo. `reset` is the private local rewrite tool.
- Before aggressive cleanup, create a named escape hatch: `git branch backup/my-branch-before-cleanup`.
- The reflog is local time travel. Use it before panicking.
- If you cannot explain where `HEAD`, your branch, the index, and the working tree point, stop and inspect.

---

## Suggested Study Plan

### Pass 1: Build The Model

1. Read `00-mental-model-and-internals.md`.
2. Run the object commands in a scratch repo.
3. Explain out loud what a commit points to.

### Pass 2: Daily Workflow With Internals

1. Read `01-local-workflow-index-and-diff.md`.
2. Practice partial staging.
3. Predict every `status` and `diff` before running it.

### Pass 3: History Surgery

1. Read `02-history-branches-merge-and-rebase.md`.
2. Practice merge conflicts and rebase conflicts.
3. Draw the commit graph before and after each operation.

### Pass 4: Recovery

1. Read `03-undo-recovery-and-reflog.md`.
2. Intentionally lose commits in a scratch repo.
3. Recover them using `reflog`.

### Pass 5: Senior Workflows

1. Read `04-remotes-collaboration-and-prs.md`.
2. Read `05-archaeology-bisect-worktree-and-advanced-tools.md`.
3. Do the labs without answers.

---

## References

- Git tutorial: https://git-scm.com/docs/gittutorial
- Git everyday commands: https://git-scm.com/docs/giteveryday
- Git workflows: https://git-scm.com/docs/gitworkflows
- Git object model commands: `git help cat-file`, `git help hash-object`, `git help update-index`
- Recovery commands: `git help reflog`, `git help reset`, `git help restore`, `git help revert`

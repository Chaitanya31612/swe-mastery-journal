# 03 - Undo, Recovery, And Reflog

This is the panic manual. Most Git damage is recoverable if you stop, inspect, and avoid stacking more destructive commands.

---

## First Rule: Classify The Undo

Before choosing a command, answer:

1. Is the bad change committed?
2. Has it been pushed?
3. Do I want to preserve history or rewrite it?
4. Do I need to keep the file changes somewhere?

Decision guide:

```text
Unstaged file change?
  git restore file

Staged but not committed?
  git restore --staged file

Bad local commit not pushed?
  git reset or git commit --amend or git rebase -i

Bad public commit?
  git revert

Lost commit?
  git reflog, then branch or reset back to it
```

---

## `git restore`

Discard unstaged changes:

```bash
git restore path/to/file
```

Unstage:

```bash
git restore --staged path/to/file
```

Restore from a specific commit:

```bash
git restore --source=HEAD~1 -- path/to/file
git restore --source=origin/main -- path/to/file
```

Mental model:

- restore copies content
- it does not create a commit
- it does not move branches

---

## `git reset`

`git reset` moves the current branch to another commit. Depending on mode, it also updates the index and working tree.

Assume:

```text
A---B---C main
        ^
        HEAD
```

Command:

```bash
git reset <target>
```

Core effect:

```text
main -> <target>
```

Modes decide what happens to index and working tree.

---

## Reset Modes

### `--soft`

```bash
git reset --soft HEAD~1
```

Moves branch only.

```text
branch:       moved back
index:        keeps changes from removed commit staged
working tree: keeps files as-is
```

Use when:

- you committed too early
- you want to recommit with a better message
- you want to combine recent local commits manually

### default mixed reset

```bash
git reset HEAD~1
git reset --mixed HEAD~1
```

Moves branch and resets index.

```text
branch:       moved back
index:        matches target commit
working tree: keeps files as-is
```

Use when:

- you want to uncommit but keep edits
- you want to split a commit

### `--hard`

```bash
git reset --hard HEAD~1
```

Moves branch, resets index, resets working tree.

```text
branch:       moved back
index:        matches target commit
working tree: matches target commit
```

Use only when:

- you truly want to discard local changes
- you have checked `git status`
- you know the target is correct

Senior habit before hard reset:

```bash
git branch backup/before-hard-reset
```

---

## `git revert`

`git revert` creates a new commit that undoes another commit.

```bash
git revert <commit-id>
```

Before:

```text
A---B---C main
```

Revert `C`:

```text
A---B---C---R main
```

`R` applies the inverse patch of `C`.

Use revert for public history because it preserves the fact that the original commit happened.

---

## Revert A Merge Commit

Merge commits have multiple parents. You must tell Git which parent is the mainline.

```bash
git revert -m 1 <merge-commit>
```

`-m 1` means "treat parent 1 as the mainline and undo what the merge introduced from the other side".

Senior caution: reverting a merge records that the merged changes should be considered undone. Re-merging the same branch later can surprise you unless new commits are added or you revert the revert.

---

## Reflog

Reflog records where refs have pointed locally.

```bash
git reflog
```

Example:

```text
abc1234 HEAD@{0}: reset: moving to HEAD~1
def5678 HEAD@{1}: commit: Add payment retry
```

Recover:

```bash
git branch recovered/payment-retry def5678
```

Or move back:

```bash
git reset --hard def5678
```

Safer first move:

```bash
git branch rescue/from-reflog def5678
```

Create a branch first. Then decide what to do.

---

## Common Recovery Scenarios

### I amended and lost the old commit

```bash
git reflog
git branch rescue/old-commit <old-commit-id>
```

### I reset too far

```bash
git reflog
git reset --hard HEAD@{1}
```

Use the actual reflog entry after inspecting.

### I committed on the wrong branch

If the commit should move to a new branch:

```bash
git branch correct-branch
git reset --hard HEAD~1
git switch correct-branch
```

If the commit should move to an existing branch:

```bash
git switch correct-branch
git cherry-pick <commit-id>
git switch wrong-branch
git reset --hard HEAD~1
```

### I deleted a branch

```bash
git reflog
git branch recovered/name <commit-id>
```

If you know the branch tip from terminal output:

```bash
git branch recovered/name <deleted-tip-id>
```

### I need one file from another branch

```bash
git restore --source=other-branch -- path/to/file
```

Then inspect and commit if desired.

---

## Clean Working Tree Without Losing Work

If you need to switch tasks fast:

```bash
git status
git switch -c wip/current-task
git add -A
git commit -m 'WIP current task'
```

Later:

```bash
git reset HEAD~1
```

This returns the WIP commit changes to your working tree.

Alternative:

```bash
git stash push -u -m 'WIP current task'
```

Prefer WIP branches for work you might care about. Prefer stash for short interruptions.

---

## `git clean`

`git clean` removes untracked files.

Preview first:

```bash
git clean -nd
```

Remove:

```bash
git clean -fd
```

Include ignored files:

```bash
git clean -fdx
```

Senior warning: `git clean -fdx` can delete build output, local env files, downloaded assets, and anything ignored. Preview first.

---

## Public vs Private Undo

Private local branch:

```bash
git commit --amend
git reset
git rebase -i
```

Shared branch:

```bash
git revert
git merge
```

Shared branch with agreed rewrite:

```bash
git push --force-with-lease
```

Prefer `--force-with-lease` over `--force`.

`--force-with-lease` refuses to overwrite remote work you have not fetched.

---

## Panic Checklist

When something goes wrong:

```bash
git status
git log --oneline --graph --decorate --all -30
git reflog -30
```

Then:

1. Do not run another destructive command yet.
2. Create a rescue branch at the commit you might need.
3. Decide whether the undo is private or public.
4. Use the least destructive command that solves it.

The senior move is not being fearless. It is making recovery points before surgery.

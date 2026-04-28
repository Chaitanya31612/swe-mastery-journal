# 02 - History, Branches, Merge, And Rebase

This is where Git becomes a graph editor. Branches are names. Commits are immutable nodes. Merge, rebase, and cherry-pick are different ways to create new graph shapes.

---

## Branches Are Movable Names

Create a branch:

```bash
git branch feature/reporting
```

This creates a ref pointing to the current commit.

```text
A---B main
     \
      feature/reporting
```

Switch to it:

```bash
git switch feature/reporting
```

Now `HEAD` points to that branch.

```text
HEAD -> feature/reporting -> B
```

Commit:

```bash
git commit -m 'Add report filter'
```

The branch moves:

```text
A---B main
     \
      C feature/reporting
```

Senior intuition: commits do not know branch names. Branch names know commits.

---

## `git switch` vs `git checkout`

Modern Git split checkout into clearer commands:

```bash
git switch branch-name
git switch -c new-branch
git restore file.txt
```

Older form:

```bash
git checkout branch-name
git checkout -b new-branch
git checkout -- file.txt
```

Use `switch` and `restore` for clarity. Know `checkout` because old docs and scripts use it.

---

## Merge

`git merge other` integrates another branch into the current branch.

Fast-forward merge:

```text
A---B main
     \
      C---D feature
```

If `main` has not moved since `feature` branched:

```bash
git switch main
git merge feature
```

Result:

```text
A---B---C---D main
            ^
            feature
```

No merge commit needed. Git just moves `main`.

---

## True Merge Commit

If both branches moved:

```text
A---B---C main
     \
      D---E feature
```

Merge:

```bash
git switch main
git merge feature
```

Result:

```text
A---B---C---M main
     \     /
      D---E feature
```

Merge commit `M` has two parents:

- first parent: previous `main`
- second parent: `feature`

Senior intuition: merge preserves the fact that parallel work happened.

---

## Merge Strategy Basics

Modern Git usually uses the `ort` merge strategy for normal branch merges.

Conceptually, a three-way merge uses:

```text
base   -> common ancestor
ours   -> current branch
theirs -> branch being merged
```

Git asks:

- what changed from base to ours?
- what changed from base to theirs?
- can those changes be combined automatically?

Conflict happens when Git cannot safely combine both edits.

---

## Conflict Markers

Conflict markers:

```text
<<<<<<< HEAD
current branch version
=======
incoming branch version
>>>>>>> feature
```

Resolve by editing the file to the final desired content, then:

```bash
git add conflicted-file.txt
git merge --continue
```

Or abort:

```bash
git merge --abort
```

Senior conflict process:

1. Identify intent of both sides.
2. Decide final behavior, not just final text.
3. Run tests or at least inspect affected paths.
4. Stage resolved files.
5. Continue merge.

---

## Rebase

`git rebase base` takes commits from the current branch that are not in `base`, then replays them on top of `base`.

Before:

```text
A---B---C main
     \
      D---E feature
```

Command:

```bash
git switch feature
git rebase main
```

After:

```text
A---B---C main
         \
          D'---E' feature
```

`D'` and `E'` are new commits. Same patches in spirit, new object ids.

Senior intuition: rebase rewrites commits. It does not move the old commits. It creates replacement commits and moves the branch name.

---

## Merge vs Rebase

Use merge when:

- branch topology matters
- integrating a shared branch
- you want a non-rewritten record of parallel development
- the branch was already published and others built on it

Use rebase when:

- cleaning your private branch
- updating feature work on top of latest main
- preparing a clean PR
- splitting or reordering local commits

Bad senior smell: "always rebase" or "never rebase". The right answer depends on ownership and history value.

---

## Interactive Rebase

Use interactive rebase to edit local commit history.

```bash
git rebase -i main
```

Common actions:

```text
pick    keep commit
reword  keep commit but edit message
edit    stop at commit so you can change it
squash  combine into previous commit and edit message
fixup   combine into previous commit and discard this message
drop    remove commit
```

Practical uses:

- squash noisy WIP commits
- reword vague messages
- split a commit
- reorder independent commits
- remove accidental debug commits

Senior caution: do not interactive-rebase shared public history unless explicitly coordinated.

---

## Splitting A Commit

Start:

```bash
git rebase -i main
```

Mark the commit as `edit`.

When Git stops:

```bash
git reset HEAD^
git add -p
git commit -m 'First logical change'
git add -p
git commit -m 'Second logical change'
git rebase --continue
```

Why this works:

- `git reset HEAD^` moves branch back one commit
- default mixed reset keeps working tree changes
- you restage and recommit in smaller units

---

## Autosquash

Create a fixup commit:

```bash
git commit --fixup <commit-id>
```

Then:

```bash
git rebase -i --autosquash main
```

Git automatically places the fixup next to its target and marks it as `fixup`.

Senior habit: use `--fixup` during review fixes so cleanup is mechanical.

---

## Cherry-Pick

`git cherry-pick` replays selected commits onto the current branch.

```bash
git switch release/1.4
git cherry-pick <bugfix-commit>
```

Before:

```text
A---B---C---D main
     \
      R release/1.4
```

After:

```text
A---B---C---D main
     \
      R---D' release/1.4
```

Use for:

- backporting a fix
- applying one commit without merging the whole branch
- moving a small patch across branches

Do not use cherry-pick as a default integration strategy for long-running branches. It duplicates commits and can create confusing future merges.

---

## Rebase Conflicts

During rebase, Git replays commits one at a time.

Conflict flow:

```bash
git status
# edit files
git add resolved-file.txt
git rebase --continue
```

Abort:

```bash
git rebase --abort
```

Skip current commit:

```bash
git rebase --skip
```

Senior intuition: in rebase conflict messages, "ours" and "theirs" can feel inverted. You are applying your commit onto the new base. Read `git status` carefully.

---

## Range Notation For History

Commits reachable from `feature` but not from `main`:

```bash
git log main..feature
```

Commits on either side since divergence:

```bash
git log main...feature
```

Find merge base:

```bash
git merge-base main feature
```

Show branch contribution:

```bash
git log --oneline main..HEAD
git diff main...HEAD
```

These are daily senior commands for PR cleanup.

---

## Designing A Clean PR History

Before opening or updating a PR:

```bash
git fetch origin
git switch feature/my-work
git rebase origin/main
git log --oneline origin/main..HEAD
git diff origin/main...HEAD
```

Then ask:

- Does each commit compile or make sense independently?
- Are review fixes squashed into the commits they fix?
- Are generated files separated from hand-written logic if that helps review?
- Are accidental unrelated changes removed?
- Does the PR diff match the story I intend to tell?

Senior Git is partly history design. You are making future debugging easier.

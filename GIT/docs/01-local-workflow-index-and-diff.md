# 01 - Local Workflow, Index, And Diff

This doc is about the daily loop: edit, inspect, stage, commit. The senior skill is not knowing more commands. It is knowing exactly which snapshot each command compares or mutates.

---

## The Local State Machine

```text
HEAD commit
  Last committed snapshot.

index
  Snapshot that will become the next commit.

working tree
  Files on disk.
```

The same file can exist in three different versions at once:

```text
HEAD:         old committed version
index:        staged version
working tree: currently edited version
```

This is not an edge case. This is normal Git.

---

## `git status`

`git status` answers:

- What branch am I on?
- What is staged for commit?
- What is modified but not staged?
- What is untracked?
- Is my local branch ahead or behind its upstream?

Useful forms:

```bash
git status
git status --short
git status --branch --short
```

Short status examples:

```text
 M file.txt
M  staged.txt
MM split.txt
?? new.txt
```

Read it as two columns:

```text
XY path
```

- `X` = index status
- `Y` = working tree status

Examples:

```text
 M file.txt
```

Modified in working tree only.

```text
M  staged.txt
```

Modified in index. Ready to commit.

```text
MM split.txt
```

One version is staged, then the file was modified again.

---

## `git add`

`git add` copies content from the working tree into the index.

It does not mean "start tracking forever" only. It means "make the index match this working tree content for these paths".

Common forms:

```bash
git add file.txt
git add src/
git add -A
git add -p
```

Use `git add -p` when a file contains more than one logical change.

Senior rule: commits should be reviewable units of intent. `git add -p` is the scalpel.

---

## Partial Staging

Example:

```bash
printf 'line 1\nline 2\nline 3\n' > notes.txt
git add notes.txt
git commit -m 'Add notes'

sed -i 's/line 1/line one/' notes.txt
sed -i 's/line 3/line three/' notes.txt
git add -p notes.txt
```

Git asks whether to stage hunks.

Common choices:

```text
y  stage this hunk
n  do not stage this hunk
s  split this hunk
e  manually edit this hunk
q  quit
?  help
```

After partial staging:

```bash
git diff
git diff --cached
```

You may see changes in both places for the same file.

That is not dirty Git. That is disciplined Git.

---

## The Diff Family

### Working Tree vs Index

```bash
git diff
```

Question: "What have I changed but not staged?"

### Index vs HEAD

```bash
git diff --cached
git diff --staged
```

Question: "What will the next commit contain?"

### Working Tree vs HEAD

```bash
git diff HEAD
```

Question: "What is everything changed since the last commit?"

### Commit vs Commit

```bash
git diff main..feature
git diff main feature
```

Question: "How do these two endpoint trees differ?"

### Merge Base vs Branch

```bash
git diff main...feature
```

Question: "What did feature change since it branched from main?"

This matters in PR review. Most PR diffs are conceptually a three-dot diff.

---

## Two-Dot vs Three-Dot

Assume:

```text
A---B---C main
     \
      D---E feature
```

Two-dot:

```bash
git diff main..feature
```

Compares endpoint `C` to endpoint `E`.

Three-dot:

```bash
git diff main...feature
```

Compares merge base `B` to endpoint `E`.

Senior intuition:

- use two-dot when you care about final tree difference
- use three-dot when you care about branch contribution

---

## `git commit`

`git commit` writes the index as a new commit.

Useful forms:

```bash
git commit
git commit -m 'Message'
git commit --amend
git commit --fixup <commit>
```

`--amend` does not edit a commit in place. It creates a new commit with a new id and moves the branch to it.

Before amend:

```text
A---B main
```

After amend:

```text
A---B' main
 \
  B  no longer named by main
```

Use amend freely on local private commits. Be careful after push.

---

## Commit Message Quality

A senior commit message explains why the change exists.

Weak:

```text
Update files
```

Better:

```text
Validate import rows before persistence

Reject malformed rows before opening a transaction so partial imports cannot
leave mixed valid and invalid records behind.
```

Practical format:

```text
<imperative summary>

<why this change exists>
<important trade-offs or migration notes>
```

Good summaries:

- `Fix stale cache reads after account merge`
- `Add import row validation before persistence`
- `Split billing retry policy from gateway client`
- `Document Git recovery workflow`

---

## `git restore`

`git restore` copies content from a source into the working tree or index.

Discard unstaged changes:

```bash
git restore file.txt
```

Unstage while keeping working tree changes:

```bash
git restore --staged file.txt
```

Restore file from another commit:

```bash
git restore --source=main -- path/to/file
git restore --source=HEAD~2 -- path/to/file
```

Mental model:

```text
git restore file
  source: index
  destination: working tree

git restore --staged file
  source: HEAD
  destination: index
```

---

## `git rm` And `git mv`

These are convenience commands for index-aware file operations.

```bash
git rm old.txt
git mv old_name.txt new_name.txt
```

Equivalent idea:

```text
change working tree
stage the deletion/addition in index
```

Git does not need `git mv` to detect renames. It often infers renames from content similarity. `git mv` is still useful because it updates working tree and index in one command.

---

## Ignore Rules

Ignore rules affect untracked files.

They do not stop Git from tracking files already committed.

Common files:

```text
.gitignore
.git/info/exclude
global excludes file
```

If a tracked file should become ignored:

```bash
git rm --cached path/to/file
```

Then add the ignore rule and commit both.

Senior caution: never casually commit generated files, secrets, local env files, or editor state. If a secret was committed, removing it in a later commit is not enough. The secret still exists in history.

---

## Stash

`git stash` stores working tree and index changes as commits under a special ref.

Useful forms:

```bash
git stash push -m 'WIP before rebase'
git stash push -u -m 'Include untracked files'
git stash list
git stash show -p stash@{0}
git stash apply stash@{0}
git stash pop
git stash drop stash@{0}
```

`apply` keeps the stash.

`pop` applies and drops if successful.

Senior preference: for serious work, create a WIP commit or temporary branch instead of leaning too hard on stash.

```bash
git switch -c wip/payment-retry
git add -A
git commit -m 'WIP payment retry experiment'
```

WIP commits are visible, nameable, and easier to recover.

---

## Daily Local Workflow

Use this loop:

```bash
git status --short --branch
git diff
git add -p
git diff --cached
git commit
git log --oneline --decorate -5
```

Before pushing:

```bash
git fetch origin
git log --oneline --graph --decorate --all -20
git diff origin/main...HEAD
```

Senior habit: review your own diff as if you are the reviewer.

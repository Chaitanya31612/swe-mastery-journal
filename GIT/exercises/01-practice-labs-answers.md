# 01 - Git Practice Labs Answers

These answers prefer explicit commands over shortcuts so the mechanics stay visible.

---

## Lab 1 Answer: See The Three Trees

```bash
mkdir lab-01-three-trees
cd lab-01-three-trees
git init

printf 'one\n' > file.txt
git add file.txt
git commit -m 'Add one'

printf 'two\n' > file.txt
git add file.txt

printf 'three\n' > file.txt

git diff
git diff --cached
git show HEAD:file.txt
git show :file.txt
cat file.txt
```

Answers:

- `git commit` would store `two`, because the index contains `two`.
- `git diff` shows `two -> three`, because it compares index to working tree.
- `git diff --cached` shows `one -> two`, because it compares `HEAD` to index.

---

## Lab 2 Answer: Write And Inspect Git Objects

```bash
mkdir ../lab-02-objects
cd ../lab-02-objects
git init

printf 'hello git\n' > note.txt

git hash-object note.txt
blob_id=$(git hash-object -w note.txt)

git cat-file -t "$blob_id"
git cat-file -p "$blob_id"

git add note.txt
tree_id=$(git write-tree)

git cat-file -t "$tree_id"
git cat-file -p "$tree_id"

git commit -m 'Add note'
commit_id=$(git rev-parse HEAD)

git cat-file -t "$commit_id"
git cat-file -p "$commit_id"
```

Answers:

- The blob does not know the filename. It only stores bytes.
- The filename is stored in the tree object.
- The commit points to a root tree and parent commits. The first commit has no parent.

---

## Lab 3 Answer: Partial Staging

```bash
mkdir ../lab-03-partial-staging
cd ../lab-03-partial-staging
git init

printf 'alpha\nbeta\ngamma\n' > app.txt
git add app.txt
git commit -m 'Add app text'

sed -i 's/alpha/ALPHA/' app.txt
sed -i 's/gamma/GAMMA/' app.txt

git add -p app.txt
git diff --cached
git commit -m 'Capitalize alpha'

git status --short
git diff
```

If Git shows both edits in one hunk, use `s` to split. If it cannot split cleanly, use `e` and manually keep only the line 1 change in the staged patch.

Answers:

- `git add -p` stages part of a file.
- `git diff --cached` proves the staged patch.
- `git diff` proves the remaining unstaged patch.

---

## Lab 4 Answer: Two-Dot vs Three-Dot Diff

```bash
mkdir ../lab-04-dot-diff
cd ../lab-04-dot-diff
git init

printf 'A\n' > story.txt
git add story.txt
git commit -m 'A'
git branch -M main

printf 'A\nB\n' > story.txt
git add story.txt
git commit -m 'B'

git switch -c feature
printf 'A\nB\nD\n' > story.txt
git add story.txt
git commit -m 'D'

git switch main
printf 'A\nB\nC\n' > story.txt
git add story.txt
git commit -m 'C'

git diff main..feature
git diff main...feature
git log --oneline main..feature
git log --oneline main...feature
```

Answers:

- `git diff main...feature` resembles a PR diff because it compares the merge base to `feature`.
- The diffs differ because `main..feature` compares endpoint trees, while `main...feature` compares branch contribution since divergence.

---

## Lab 5 Answer: Merge Conflict

```bash
mkdir ../lab-05-merge-conflict
cd ../lab-05-merge-conflict
git init

printf 'color=blue\n' > config.txt
git add config.txt
git commit -m 'Add blue config'
git branch -M main

git switch -c feature
printf 'color=green\n' > config.txt
git add config.txt
git commit -m 'Change color to green'

git switch main
printf 'color=red\n' > config.txt
git add config.txt
git commit -m 'Change color to red'

git merge feature

printf 'color=purple\n' > config.txt
git add config.txt
git merge --continue

git log --oneline --graph --decorate --all
```

Answers:

- Merge base is the commit where `color=blue`.
- Ours is current branch `main`, with `color=red`.
- Theirs is `feature`, with `color=green`.
- Git needed help because both branches changed the same line from the same base.

---

## Lab 6 Answer: Rebase Conflict

```bash
mkdir ../lab-06-rebase-conflict
cd ../lab-06-rebase-conflict
git init

printf 'color=blue\n' > config.txt
git add config.txt
git commit -m 'Add blue config'
git branch -M main

git switch -c feature
printf 'color=green\n' > config.txt
git add config.txt
git commit -m 'Change color to green'

git switch main
printf 'color=red\n' > config.txt
git add config.txt
git commit -m 'Change color to red'

git switch feature
old_feature_commit=$(git rev-parse HEAD)

git rebase main

printf 'color=purple\n' > config.txt
git add config.txt
git rebase --continue

new_feature_commit=$(git rev-parse HEAD)
printf 'old=%s\nnew=%s\n' "$old_feature_commit" "$new_feature_commit"
git log --oneline --graph --decorate --all
```

Answers:

- Git did not create a merge commit.
- The feature commit id changed because rebase created a new commit on top of `main`.
- During rebase, Git is replaying your commit onto the new base. The labels can feel inverted because the temporary merge context is not the same as normal branch merge intuition.

---

## Lab 7 Answer: Reset Modes

```bash
mkdir ../lab-07-reset-modes
cd ../lab-07-reset-modes
git init

printf 'A\n' > file.txt
git add file.txt
git commit -m 'A'

printf 'A\nB\n' > file.txt
git add file.txt
git commit -m 'B'

printf 'A\nB\nC\n' > file.txt
git add file.txt
git commit -m 'C'

git branch rescue/original

git reset --soft HEAD~1
git status --short
git log --oneline --decorate -3

git reset --hard rescue/original

git reset HEAD~1
git status --short
git log --oneline --decorate -3

git reset --hard rescue/original

git reset --hard HEAD~1
git status --short
git log --oneline --decorate -3
cat file.txt
```

Answers:

- `--soft` keeps changes staged.
- default mixed reset keeps changes unstaged.
- `--hard` discards file changes by making index and working tree match the target commit.

---

## Lab 8 Answer: Recover A Lost Commit

```bash
mkdir ../lab-08-reflog-recovery
cd ../lab-08-reflog-recovery
git init

printf 'A\n' > file.txt
git add file.txt
git commit -m 'A'

printf 'A\nB\n' > file.txt
git add file.txt
git commit -m 'B'

printf 'A\nB\nC\n' > file.txt
git add file.txt
git commit -m 'C'

c_commit=$(git rev-parse HEAD)

git reset --hard HEAD~2
git log --oneline

git reflog
git branch recovered/c "$c_commit"
git log --oneline --decorate --all
```

If you did not save the id, copy it from `git reflog`:

```bash
git branch recovered/c <commit-id-from-reflog>
```

Answers:

- `C` was not deleted immediately. It became unreachable from the current branch but remained in the object database and reflog.
- `git branch recovered/c <commit-id>` made it reachable again.

---

## Lab 9 Answer: Revert Public History

```bash
mkdir ../lab-09-revert
cd ../lab-09-revert
git init

printf 'A\n' > file.txt
git add file.txt
git commit -m 'A'

printf 'A\nB\n' > file.txt
git add file.txt
git commit -m 'B'

printf 'A\nB\nC\n' > file.txt
git add file.txt
git commit -m 'C'

git revert --no-edit HEAD

git log --oneline --decorate
cat file.txt
git show --stat HEAD
```

Answers:

- Revert is safer on shared branches because it does not move existing history backward. It adds a new commit.
- The revert commit contains the inverse patch of `C`.

---

## Lab 10 Answer: Cherry-Pick A Hotfix

```bash
mkdir ../lab-10-cherry-pick
cd ../lab-10-cherry-pick
git init

printf 'A\n' > app.txt
git add app.txt
git commit -m 'A'
git branch -M main

git branch release/1.0

printf 'A\nB\n' > app.txt
git add app.txt
git commit -m 'B'

printf 'feature=true\n' > feature.txt
git add feature.txt
git commit -m 'C feature'

printf 'fix=true\n' > fix.txt
git add fix.txt
git commit -m 'D bugfix'

bugfix_commit=$(git rev-parse HEAD)

git switch release/1.0
git cherry-pick "$bugfix_commit"

git log --oneline --decorate --all --graph
ls
```

Answers:

- `release/1.0` received only the bugfix patch, not the feature commit.
- The cherry-picked commit has a different id because it is a new commit with a different parent.

---

## Lab 11 Answer: Bisect A Regression

```bash
mkdir ../lab-11-bisect
cd ../lab-11-bisect
git init

cat > check.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail

if grep -q 'broken' app.txt; then
  exit 1
fi

exit 0
SH
chmod +x check.sh

printf 'ok\n' > app.txt
git add app.txt check.sh
git commit -m 'A good'

printf 'still ok\n' > app.txt
git add app.txt
git commit -m 'B good'

printf 'broken\n' > app.txt
git add app.txt
git commit -m 'C bad'

printf 'broken with more changes\n' > app.txt
git add app.txt
git commit -m 'D still bad'

git bisect start
git bisect bad
git bisect good HEAD~3
git bisect run ./check.sh
git bisect reset
```

Answers:

- Exit `0` means good.
- Exit non-zero, commonly `1`, means bad. Exit `125` means skip.
- Automation is better because it removes judgment drift and lets Git search quickly and repeatably.

---

## Lab 12 Answer: Worktree Hotfix

```bash
mkdir ../lab-12-worktree
cd ../lab-12-worktree
git init

printf 'stable\n' > app.txt
git add app.txt
git commit -m 'Stable app'
git branch -M main

git switch -c feature/dirty-work
printf 'dirty feature work\n' > feature.txt

git worktree add -b hotfix/login-timeout ../lab-12-hotfix main

cd ../lab-12-hotfix
printf 'hotfix\n' > hotfix.txt
git add hotfix.txt
git commit -m 'Fix login timeout'

cd ../lab-12-worktree
git status --short
git worktree list
```

Answers:

- Worktree is better here because dirty feature work remains untouched while the hotfix gets its own working directory, branch, and index.
- `git worktree list` lists active worktrees.

---

## Lab 13 Answer: Force-With-Lease Reasoning

```bash
mkdir ../lab-13-force-lease
cd ../lab-13-force-lease

git init --bare remote.git
git clone remote.git alice
git clone remote.git bob

cd alice
printf 'base\n' > app.txt
git add app.txt
git commit -m 'Base'
git push -u origin HEAD:main

git switch -c feature/shared
printf 'alice 1\n' > alice.txt
git add alice.txt
git commit -m 'Alice work'
git push -u origin feature/shared

cd ../bob
git fetch origin
git switch -c feature/shared origin/feature/shared
printf 'bob work\n' > bob.txt
git add bob.txt
git commit -m 'Bob work'
git push

cd ../alice
git commit --amend -m 'Alice work rewritten'

git push
git push --force-with-lease

git fetch origin
git log --oneline --graph --decorate --all
```

Expected:

- normal push is rejected as non-fast-forward
- `--force-with-lease` should also reject before Alice fetches because `origin/feature/shared` in Alice's repo is stale

Answers:

- Alice's force-with-lease should fail because the remote branch no longer points to the commit Alice last fetched.
- Bob's commit was protected from being overwritten by Alice's stale rewrite.

---

## Lab 14 Answer: Find Why A Line Changed

```bash
mkdir ../lab-14-archaeology
cd ../lab-14-archaeology
git init

cat > config.txt <<'EOF'
timeout=10
retries=1
EOF
git add config.txt
git commit -m 'Add initial config'

sed -i 's/timeout=10/timeout=20/' config.txt
git add config.txt
git commit -m 'Increase timeout for slow network'

sed -i 's/retries=1/retries=3/' config.txt
git add config.txt
git commit -m 'Increase retry count'

git blame config.txt
timeout_commit=$(git log --format=%H -S 'timeout=20' -- config.txt | head -n 1)
git show "$timeout_commit"
git log -p -S 'timeout=20' -- config.txt
```

Answers:

- Blame tells which final-line commit last touched each line.
- Pickaxe tells when a string was introduced or removed, which can reveal earlier context even after later edits or moves.

---

## Lab 15 Answer: Clean PR Preparation

```bash
mkdir ../lab-15-clean-pr
cd ../lab-15-clean-pr
git init

printf 'base\n' > app.txt
git add app.txt
git commit -m 'Base'
git branch -M main

git switch -c feature/clean-history

printf 'base\nfeature\n' > app.txt
git add app.txt
git commit -m 'Add feature behavior'
feature_commit=$(git rev-parse HEAD)

printf 'base\nfeature fixed typo\n' > app.txt
git add app.txt
git commit --fixup "$feature_commit"

printf 'debug=true\n' > debug.txt
git add debug.txt
git commit -m 'Temporary debug change'

git rebase -i --autosquash main
```

In the editor:

- keep the feature commit
- keep the fixup attached to it
- drop the temporary debug commit

Then inspect:

```bash
git log --oneline main..HEAD
git diff main...HEAD
```

Answers:

- `git log --oneline main..HEAD` shows commits unique to your branch.
- `git diff main...HEAD` shows the PR-style branch contribution.
- Cleanup is acceptable before push because no one else depends on those commit ids. It is risky after others depend on the branch because rebase replaces commits with new ids.

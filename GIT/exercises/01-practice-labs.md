# 01 - Git Practice Labs

Use a scratch directory. Do not run these inside an important repository unless the lab explicitly says it is inspection-only.

Recommended setup:

```bash
mkdir -p /tmp/git-mastery-labs
cd /tmp/git-mastery-labs
```

Answers are in `01-practice-labs-answers.md`.

---

## Lab 1: See The Three Trees

Goal: prove that `HEAD`, index, and working tree can hold different versions of the same file.

Tasks:

1. Create a repo.
2. Commit `file.txt` containing `one`.
3. Change it to `two` and stage it.
4. Change it again to `three` without staging.
5. Show:
   - unstaged diff
   - staged diff
   - committed version
   - staged version
   - working tree version

Questions:

- Which version would `git commit` store?
- Which command shows `two -> three`?
- Which command shows `one -> two`?

---

## Lab 2: Write And Inspect Git Objects

Goal: understand blob, tree, and commit objects.

Tasks:

1. Create a repo.
2. Create `note.txt`.
3. Use `git hash-object` before staging.
4. Write the blob object.
5. Stage the file.
6. Use `git write-tree`.
7. Commit.
8. Inspect the commit, tree, and blob with `git cat-file`.

Questions:

- Does the blob know the filename?
- Where is the filename stored?
- What does the commit point to?

---

## Lab 3: Partial Staging

Goal: create one file with two logical edits and commit only one.

Tasks:

1. Create and commit `app.txt` with three lines.
2. Edit line 1 and line 3.
3. Stage only the line 1 change.
4. Commit it.
5. Confirm line 3 is still uncommitted.

Questions:

- Which command lets you stage part of a file?
- Which diff proves the staged patch?
- Which diff proves the unstaged patch?

---

## Lab 4: Two-Dot vs Three-Dot Diff

Goal: see endpoint diff vs branch contribution diff.

Tasks:

1. Create `main` with commits `A` and `B`.
2. Branch `feature` from `B`.
3. Add commit `D` on `feature`.
4. Switch back to `main` and add commit `C`.
5. Compare:
   - `git diff main..feature`
   - `git diff main...feature`
   - `git log main..feature`
   - `git log main...feature`

Questions:

- Which diff resembles a PR diff?
- Why can the two diffs differ?

---

## Lab 5: Merge Conflict

Goal: resolve a real three-way merge conflict.

Tasks:

1. Create a file with `color=blue`.
2. Branch `feature`.
3. On `feature`, change it to `color=green`.
4. On `main`, change it to `color=red`.
5. Merge `feature` into `main`.
6. Resolve final value as `color=purple`.
7. Complete the merge.

Questions:

- What is the merge base?
- What is ours?
- What is theirs?
- Why did Git need help?

---

## Lab 6: Rebase Conflict

Goal: understand conflict flow during rebase.

Tasks:

1. Build the same conflict shape as Lab 5.
2. Instead of merging, rebase `feature` onto `main`.
3. Resolve final value as `color=purple`.
4. Continue the rebase.

Questions:

- Did Git create a merge commit?
- Did the feature commit id change?
- Why can "ours" and "theirs" feel confusing during rebase?

---

## Lab 7: Reset Modes

Goal: compare `--soft`, mixed, and `--hard`.

Tasks:

1. Create three commits: `A`, `B`, `C`.
2. Create a rescue branch.
3. Run `git reset --soft HEAD~1`.
4. Inspect status and log.
5. Return to rescue branch state.
6. Run mixed reset.
7. Inspect status and log.
8. Return to rescue branch state.
9. Run hard reset.
10. Inspect status and log.

Questions:

- Which mode keeps changes staged?
- Which mode keeps changes unstaged?
- Which mode discards file changes?

---

## Lab 8: Recover A Lost Commit

Goal: use reflog as local time travel.

Tasks:

1. Create commits `A`, `B`, `C`.
2. Save the id of `C`.
3. Run `git reset --hard HEAD~2`.
4. Confirm `C` is gone from normal log.
5. Find `C` in the reflog.
6. Recover it with a new branch.

Questions:

- Was commit `C` deleted immediately?
- Which command made it reachable again?

---

## Lab 9: Revert Public History

Goal: undo a commit without rewriting history.

Tasks:

1. Create commits `A`, `B`, `C`.
2. Revert `C`.
3. Inspect log.
4. Inspect file content.

Questions:

- Why is revert safer than reset on shared branches?
- What does the revert commit contain?

---

## Lab 10: Cherry-Pick A Hotfix

Goal: move one fix commit to a release branch.

Tasks:

1. Create `main` with `A`, `B`.
2. Create `release/1.0` from `A`.
3. On `main`, add feature commit `C`.
4. On `main`, add bugfix commit `D`.
5. Cherry-pick only `D` onto `release/1.0`.

Questions:

- Did release receive `C`?
- Did the cherry-picked commit keep the same id?

---

## Lab 11: Bisect A Regression

Goal: find the commit that introduced a failing behavior.

Tasks:

1. Create a small shell script `check.sh` that fails when `app.txt` contains `broken`.
2. Create several commits where one changes `app.txt` to `broken`.
3. Run `git bisect`.
4. Use `git bisect run ./check.sh`.
5. Reset bisect.

Questions:

- What exit code means good?
- What exit code means bad?
- Why is automation better than manual testing here?

---

## Lab 12: Worktree Hotfix

Goal: handle an urgent fix without disturbing dirty feature work.

Tasks:

1. Create a repo with `main`.
2. Create `feature/dirty-work`.
3. Modify files but do not commit.
4. Add a worktree from `main` into a sibling directory.
5. Create a hotfix branch in that worktree.
6. Commit a hotfix there.
7. Return to the original working tree and confirm dirty work is untouched.

Questions:

- Why is worktree better than stash for this case?
- What command lists active worktrees?

---

## Lab 13: Force-With-Lease Reasoning

Goal: understand why `--force-with-lease` exists.

Tasks:

1. Create a bare repo to act as remote.
2. Clone it twice as `alice` and `bob`.
3. Alice pushes a feature branch.
4. Bob fetches and pushes another commit to the same feature branch.
5. Alice rewrites her local feature branch.
6. Alice tries normal push.
7. Alice tries `--force-with-lease`.
8. Alice fetches, inspects, then decides how to integrate.

Questions:

- Why should Alice's force-with-lease fail before fetching?
- What remote work was protected?

---

## Lab 14: Find Why A Line Changed

Goal: combine blame, show, and pickaxe.

Tasks:

1. Create a file with a function or config value.
2. Change it across several commits.
3. Use `git blame` on the final file.
4. Use `git show` on the blamed commit.
5. Use `git log -S` to find when a string was added or removed.

Questions:

- What did blame tell you?
- What did pickaxe tell you that blame did not?

---

## Lab 15: Clean PR Preparation

Goal: turn messy local commits into a reviewable branch.

Tasks:

1. Create a branch from `main`.
2. Make three commits:
   - real feature commit
   - typo fix for the feature
   - unrelated debug change
3. Use `git commit --fixup` or interactive rebase to squash the typo fix.
4. Drop the debug change.
5. Show the final branch contribution.

Questions:

- Which commands show commits unique to your branch?
- Which command shows the PR-style diff?
- Why is this cleanup acceptable before push but risky after others depend on the branch?

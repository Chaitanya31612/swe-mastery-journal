# 04 - Remotes, Collaboration, And PRs

Remote Git is not magic synchronization. It is object exchange plus ref updates. Once that clicks, `fetch`, `pull`, `push`, upstreams, and force-with-lease become predictable.

---

## Remote Concepts

A remote is a named URL.

```bash
git remote -v
```

Common default:

```text
origin  git@github.com:org/repo.git (fetch)
origin  git@github.com:org/repo.git (push)
```

Remote-tracking refs are local refs that remember what the remote looked like when you last fetched.

```text
refs/remotes/origin/main
refs/remotes/origin/feature/login
```

Important: `origin/main` is local data. It may be stale until `git fetch origin`.

---

## Fetch

```bash
git fetch origin
```

Fetch does two things:

1. downloads missing objects
2. updates remote-tracking refs like `origin/main`

It does not change your current branch or working tree.

Senior habit:

```bash
git fetch origin
git log --oneline --graph --decorate --all -30
```

Fetch first, inspect second, integrate third.

---

## Pull

`git pull` is shorthand:

```text
git fetch
then git merge
```

or, if configured:

```text
git fetch
then git rebase
```

Equivalent explicit commands:

```bash
git fetch origin
git merge origin/main
```

or:

```bash
git fetch origin
git rebase origin/main
```

Senior preference: use explicit `fetch` plus `merge` or `rebase` on important branches. Blind pull hides the graph operation.

---

## Push

```bash
git push origin feature/my-work
```

Push uploads local objects and asks the remote to move a ref.

The remote accepts if the update is fast-forward or allowed by server policy.

Fast-forward push:

```text
remote: A---B
local:  A---B---C
```

Remote can safely move from `B` to `C`.

Rejected non-fast-forward push:

```text
remote: A---B---D
local:  A---B---C
```

Remote refuses because moving to `C` would lose `D` from that branch.

---

## Upstream Branches

An upstream links your local branch to a remote-tracking branch.

Set upstream on first push:

```bash
git push -u origin feature/my-work
```

Inspect:

```bash
git branch -vv
```

After upstream is set:

```bash
git pull
git push
```

know which remote branch to use.

Senior caution: upstream convenience is useful, but still inspect when branch history matters.

---

## Remote Branch Cleanup

Delete remote branch:

```bash
git push origin --delete feature/old-work
```

Prune stale remote-tracking refs:

```bash
git fetch --prune origin
```

List merged local branches:

```bash
git branch --merged main
```

Delete merged local branch:

```bash
git branch -d feature/done
```

Force delete local branch:

```bash
git branch -D feature/abandoned
```

Use `-D` only when you know the branch is disposable or recoverable.

---

## Force Push And Force-With-Lease

After local history rewrite, normal push may be rejected:

```bash
git push
```

Safer force:

```bash
git push --force-with-lease
```

Meaning:

```text
Update the remote only if it still points where my local remote-tracking ref
believes it points.
```

This protects you from overwriting someone else's new remote commits that you have not fetched.

Use cases:

- updating your own PR after interactive rebase
- fixing local commit history before review
- removing accidental local commits from a feature branch

Do not use it on shared release or main branches unless the team explicitly coordinated it.

---

## PR Branch Workflow

Start:

```bash
git fetch origin
git switch main
git merge --ff-only origin/main
git switch -c feature/descriptive-name
```

Work:

```bash
git status --short
git add -p
git commit
```

Before PR:

```bash
git fetch origin
git rebase origin/main
git diff origin/main...HEAD
git log --oneline origin/main..HEAD
```

Push:

```bash
git push -u origin HEAD
```

After review fixes:

```bash
git add -p
git commit --fixup <target-commit>
git rebase -i --autosquash origin/main
git push --force-with-lease
```

This keeps review fixes attached to the commits they correct.

---

## Keeping A Feature Branch Updated

Option 1: rebase private feature branch.

```bash
git fetch origin
git switch feature/my-work
git rebase origin/main
git push --force-with-lease
```

Option 2: merge main into shared feature branch.

```bash
git fetch origin
git switch feature/shared-work
git merge origin/main
git push
```

Use rebase when you own the branch.

Use merge when multiple people are basing work on the branch.

---

## Fork Workflow

Common remote setup:

```text
origin   -> your fork
upstream -> canonical repository
```

Commands:

```bash
git remote add upstream git@github.com:org/repo.git
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
git switch -c feature/my-work
```

PR usually targets `upstream/main`.

Push branch to fork:

```bash
git push -u origin HEAD
```

---

## Tags And Releases

Lightweight tag:

```bash
git tag v1.2.0
```

Annotated tag:

```bash
git tag -a v1.2.0 -m 'Release v1.2.0'
```

Push tag:

```bash
git push origin v1.2.0
```

Senior preference: use annotated tags for releases. They are full objects with metadata and messages.

---

## Submodules In Collaboration

Submodules pin another repository at a specific commit.

Clone with submodules:

```bash
git clone --recurse-submodules <url>
```

Update:

```bash
git submodule update --init --recursive
```

Senior warning: submodules are precise but operationally sharp. They are fine for vendor-like dependencies, but they add workflow cost. Many teams prefer package managers, vendoring, or monorepos unless commit-level pinning is essential.

---

## Large Files

Git is optimized for source text, not large binary churn.

Options:

- Git LFS for large binary assets
- artifact storage for build outputs
- package registry for versioned deliverables
- ignore generated files when reproducible

If a large file was committed by mistake, deleting it later does not remove it from history. You need history rewriting tools and coordinated remote cleanup.

---

## Team Safety Rules

- Protect `main`.
- Require PR review for shared branches.
- Prefer `--ff-only` pulls on main-like branches.
- Do not commit secrets.
- Use `revert` for public undo.
- Use `--force-with-lease` only for owned feature branches.
- Name branches by intent: `feature/import-validation`, `fix/cache-stale-read`, `chore/remove-dead-config`.
- Keep PRs small enough that the diff can be understood in one sitting.

Senior Git is social as much as technical. The graph is shared memory for the team.

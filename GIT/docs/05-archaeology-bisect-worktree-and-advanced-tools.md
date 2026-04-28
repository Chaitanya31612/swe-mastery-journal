# 05 - Archaeology, Bisect, Worktree, And Advanced Tools

Senior Git often means answering hard questions: when did this break, why did this line change, how do I test another branch without losing my state, and how do I repair history without making things worse?

---

## Commit Archaeology

### `git log`

Useful forms:

```bash
git log --oneline --graph --decorate --all
git log --stat
git log -p
git log -- path/to/file
git log --follow -- path/to/file
```

Use `--follow` for a single file when you want Git to follow rename detection across history.

Search commit messages:

```bash
git log --grep='retry'
```

Search added or removed text:

```bash
git log -S 'function_name'
```

Search by regex in patches:

```bash
git log -G 'timeout.*retry'
```

Senior distinction:

- `-S` asks when the count of a string changed
- `-G` asks when a patch line matched a regex

---

## `git show`

Inspect one object:

```bash
git show <commit>
git show <commit>:path/to/file
git show HEAD~2
git show origin/main:README.md
```

Use this to view old file content without switching branches.

---

## `git blame`

Basic:

```bash
git blame path/to/file
```

Ignore whitespace:

```bash
git blame -w path/to/file
```

Limit lines:

```bash
git blame -L 20,80 path/to/file
```

Blame is not for assigning fault. It is for finding context.

Senior workflow:

```bash
git blame -L 40,70 app/service.rb
git show <commit-id>
git log --oneline --graph --decorate --all --ancestry-path <commit-id>..HEAD
```

Then read the PR or surrounding commits if available.

---

## Pickaxe Debugging

Find when a symbol appeared or disappeared:

```bash
git log -S 'calculate_total' -- path/to/file
```

Find commits whose patch matches a pattern:

```bash
git log -G 'calculate_.*total' -- app/
```

Show matching patch:

```bash
git log -p -S 'calculate_total'
```

This is excellent for refactors where the file moved or the obvious blame line is not enough.

---

## Bisect

`git bisect` performs binary search over history.

Start:

```bash
git bisect start
git bisect bad
git bisect good <known-good-commit>
```

Git checks out a midpoint. You test.

```bash
git bisect good
# or
git bisect bad
```

When done:

```bash
git bisect reset
```

Automated:

```bash
git bisect start
git bisect bad
git bisect good <known-good-commit>
git bisect run ./script/test-regression.sh
git bisect reset
```

Test script contract:

```text
exit 0   -> good
exit 1   -> bad
exit 125 -> skip this commit
```

Senior bisect tips:

- First reproduce the bug on current HEAD.
- Pick a known good commit that can run the same test.
- Make the test deterministic.
- If dependencies changed, script the setup or choose a narrower range.
- Use `git bisect skip` for commits that cannot be tested.

---

## Worktree

`git worktree` lets one repository have multiple working directories.

Use cases:

- test another branch without stashing
- run two long builds at once
- hotfix from main while feature work is dirty
- inspect old release code side-by-side

Create:

```bash
git worktree add ../repo-hotfix main
```

Create new branch in a worktree:

```bash
git worktree add -b hotfix/login-timeout ../repo-hotfix origin/main
```

List:

```bash
git worktree list
```

Remove:

```bash
git worktree remove ../repo-hotfix
```

Prune stale metadata:

```bash
git worktree prune
```

Senior intuition: worktree is cleaner than stash when the interruption may last more than a few minutes.

---

## Rerere

`rerere` means reuse recorded resolution.

Enable:

```bash
git config rerere.enabled true
```

When you resolve the same conflict shape again, Git can reuse your previous resolution.

Useful when:

- long-running branch repeatedly rebases on main
- repeated backports hit the same conflict
- release branches carry recurring divergence

Senior caution: still review the resolved result. Reused conflict resolution can be syntactically correct but semantically stale.

---

## Notes

Git notes attach metadata to objects without changing the object id.

```bash
git notes add -m 'Investigated during incident 142'
git notes show
git log --show-notes
```

They are not part of normal branch history. Sharing notes requires fetching/pushing notes refs explicitly.

Use notes for local or team-specific annotations when rewriting commits would be wrong.

---

## Reflog For Branch Movement Analysis

Show branch reflog:

```bash
git reflog show main
git reflog show feature/my-work
```

Show date-based selector:

```bash
git show HEAD@{yesterday}
git diff HEAD@{2.hours.ago}..HEAD
```

This is useful when the question is "what changed in my local branch this afternoon?"

---

## `git fsck`

Find dangling objects:

```bash
git fsck --lost-found
```

This is a deeper recovery tool after refs and reflogs are not enough.

Most daily recovery should start with `git reflog`, not `fsck`.

---

## Packfiles And Maintenance

Git initially writes loose objects. Later it packs them efficiently.

Maintenance commands:

```bash
git gc
git maintenance run
git count-objects -vH
```

Usually Git runs maintenance automatically. Manual use is rare unless a repository is huge or degraded.

Senior intuition: performance problems in Git repos often come from huge binary history, excessive refs, enormous working trees, or pathological file counts.

---

## Sparse Checkout

Sparse checkout lets you populate only part of the working tree.

```bash
git sparse-checkout init --cone
git sparse-checkout set services/api packages/shared
```

Useful in large monorepos.

Trade-off: some tooling assumes the full tree exists. Validate build and editor behavior before adopting it widely.

---

## Partial Clone

Partial clone can avoid downloading every blob immediately.

```bash
git clone --filter=blob:none <url>
```

Git downloads blobs on demand.

Useful for very large repositories. It depends on server support and can shift cost to later operations.

---

## Attributes

`.gitattributes` controls path-specific behavior.

Examples:

```gitattributes
*.sh text eol=lf
*.png binary
docs/** linguist-generated=false
```

Common uses:

- normalize line endings
- mark binary files
- configure custom merge drivers
- improve GitHub language stats

Senior warning: line-ending churn creates noisy diffs and painful blame. Decide normalization early.

---

## Hooks

Hooks are scripts under `.git/hooks`.

Common hooks:

```text
pre-commit
commit-msg
pre-push
post-checkout
```

Local hooks are not versioned by default. Teams often use tools to install shared hooks.

Good hook uses:

- prevent secrets
- run fast format checks
- validate commit messages
- block obvious generated-file mistakes

Bad hook uses:

- slow full test suites on every commit
- hidden behavior that developers cannot reproduce in CI
- policy that exists only locally

Senior rule: hooks are guardrails, not a substitute for CI.

---

## Advanced Inspection Aliases

These aliases are worth having somewhere in your shell or Git config, but understand them before relying on them.

```bash
git log --oneline --graph --decorate --all
git diff --check
git diff --name-status origin/main...HEAD
git log --left-right --cherry-pick --oneline main...feature
```

`--cherry-pick` helps identify equivalent patches even if commit ids differ.

Useful after rebases or cherry-picks:

```bash
git log --left-right --cherry-pick --oneline origin/main...HEAD
```

---

## Senior Debugging Playbooks

### Find when a regression started

```bash
git bisect start
git bisect bad
git bisect good <known-good>
git bisect run ./test-regression.sh
git bisect reset
```

### Understand why a line exists

```bash
git blame -L <start>,<end> path/to/file
git show <commit>
git log -S 'important_string' -- path/to/file
```

### Test a hotfix without touching current work

```bash
git fetch origin
git worktree add -b hotfix/name ../repo-hotfix origin/main
cd ../repo-hotfix
```

### Rescue after a bad rebase

```bash
git reflog
git branch rescue/before-bad-rebase <old-tip>
git reset --hard <old-tip>
```

### Compare patch-equivalent branches

```bash
git log --left-right --cherry-pick --oneline old-branch...new-branch
```

If output is empty, the branches may differ in commit ids but contain equivalent patches.

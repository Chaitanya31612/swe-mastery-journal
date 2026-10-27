# One valid repair

The test used the working tree, which contained the unstaged helper. Review git diff --cached and test the committed snapshot in a separate clean checkout/worktree. Keep the active edits safe. Add the needed helper intentionally, not every unrelated change.

**How to check:** The cached/staged diff compares the index with HEAD.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

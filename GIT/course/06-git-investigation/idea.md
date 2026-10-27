# The idea

Use history tools to answer a question, not to assign blame. log finds commits, show reads a patch, and blame points to the last change for a line.

That line may have moved during a refactor, so inspect context.

bisect narrows a regression between a known good and bad commit by testing intermediate commits. The test must be repeatable and its good/bad meaning clear.

A commit that cannot build may need to be skipped. A flaky test gives a misleading culprit.

A worktree is another checkout sharing the repository’s objects. It is useful for a review, a clean committed-snapshot test, or a hotfix while your current edits stay in place.

Each checkout still has its own working files and index. Respect branch checkout restrictions.
## Understand the idea

Use reflog to find a recent local reference movement, then name the candidate commit with a rescue branch before changing anything else. Reflog is local and expires; it does not store every unsaved file.

Use bisect only after a repeatable good/bad check exists. A flaky network dependency can make a confident wrong culprit. Verify the check against known endpoints of the search.

A worktree gives a separate checkout for the exact committed snapshot. It helps avoid accidentally testing a staged patch together with unstaged helper changes. Save needed files before removing a worktree, and use Git’s worktree commands to keep registration consistent.

# The idea

Start with the question: what must stay? Working edits, staged changes, published history, and untracked files are different things.

Inspect status and diffs, then preserve important work before experimenting.

restore copies selected content into the index or working tree depending on flags. reset can move a branch and, depending on mode, also change the index and working tree. revert creates a new commit that reverses a past change.

That usually fits a published-history repair better than moving everybody’s history.

The reflog records recent local reference movements. It can help find an old branch tip after reset or rebase.

It is local and expires. It is not a backup of every unsaved file or every other developer’s machine.
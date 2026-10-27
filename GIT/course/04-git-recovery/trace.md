# Follow the execution

A soft reset moves the branch while keeping index/working content. A mixed reset also resets the index. A hard reset can discard tracked working changes. None should be run by habit.

Recovery starts by naming the old reachable commit with a rescue branch. Inspect it separately. A deleted untracked file that was never stored in Git is outside reflog’s promise. Seek editor/filesystem backups instead.

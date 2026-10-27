# The idea

A good commit captures one reviewable reason for change. Files are not always the right unit: one file may contain a bug fix and an unrelated cleanup.

Partial staging chooses hunks or lines for the proposed snapshot.

Read both diffs before committing. The unstaged diff explains what you have not selected.

The cached diff explains what you are about to publish. A test in the working tree may use unstaged changes; that does not prove the staged snapshot works alone.

Keep temporary work with a deliberate stash or local commit before switching context. Stashes can include different combinations of tracked and untracked work depending on flags.

Inspect their contents rather than assuming every file was saved.
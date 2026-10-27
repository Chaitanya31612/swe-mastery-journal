# Follow the execution

Partial staging updates only the chosen parts of the index. The file in your editor can still contain both changes. Unstaging copies the HEAD version back into the index while keeping the working edit for this command form.

Before claiming a staged commit passes tests, inspect it in a disposable clean checkout or worktree after committing locally. Do not run a destructive cleanup on your active work just to get a clean test environment.

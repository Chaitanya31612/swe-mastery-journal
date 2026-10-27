# The idea

A remote is a named location. origin/main is a local remote-tracking reference updated by fetch; it is not a live window into the server. Your main branch is a different local label.

fetch downloads objects and updates remote-tracking information. It does not normally merge changes into your checked-out branch. pull adds an integration step, with behavior affected by configuration and flags.

Be explicit about merge, rebase, or fast-forward-only when the choice matters.

A pull request is a review boundary. Keep the change small, explain the trigger and resulting behavior, and show validation.

A force-with-lease push checks expected remote state; it does not guarantee no collaborator depends on rewritten commits.
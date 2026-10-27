# The idea

Merge joins histories. A merge commit can have two parents and preserve both lines of development. A fast-forward just moves a branch label when no divergent history needs joining.

Rebase replays commits onto a different base, creating new commit identities. It can make a private sequence easier to review. Rewriting commits that teammates already depend on needs explicit coordination. A clean graph is not worth surprising other users.

A conflict means Git cannot safely choose content automatically. The correct resolution comes from the intended behavior of both changes. Removing markers without testing that behavior is not enough. During rebase, “ours” and “theirs” can be counterintuitive; inspect the actual versions.

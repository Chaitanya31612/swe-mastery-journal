## Break it and reason about the repair

Creating a timer without clearing it can keep updating a vanished view. A composable that silently reads route, store, and global user state is harder to reuse than one with explicit dependencies.

**Remember:** Inputs visible. State owned. Effects cleaned up.

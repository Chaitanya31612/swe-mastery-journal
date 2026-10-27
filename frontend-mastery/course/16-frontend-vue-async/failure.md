## Break it and reason about the repair

Putting onWatcherCleanup after await can miss the synchronous registration requirement. Debouncing alone still allows two requests to overlap.

**Remember:** Cleanup revokes ownership, not just network work.

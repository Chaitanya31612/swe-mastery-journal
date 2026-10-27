## Break it and reason about the repair

Watching a computed merely to copy it into another ref creates two sources. Mutating a raw object behind a proxy can bypass the access path you expected Vue to track.

**Remember:** Track the read. Batch the DOM. Wait for the right boundary.

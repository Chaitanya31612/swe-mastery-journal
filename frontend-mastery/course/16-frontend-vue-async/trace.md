## Trace the execution

Query A starts and owns active=true. Query B invalidates A: cleanup sets A inactive and aborts it.

B becomes the owner. If A finishes later, its active check prevents every visible update.

Test success-success in reverse order, stale failure after success, abort, and unmount. Give each request a controlled deferred response so the test chooses the timeline.
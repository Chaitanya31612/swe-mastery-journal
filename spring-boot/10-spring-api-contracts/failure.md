## Break it and reason about the repair

PUT/POST method names alone do not implement idempotence. Cursor encoding is not encryption or access control.

A 200 containing an error object confuses clients.

**Remember:** A retry is the same command only when you can identify it.
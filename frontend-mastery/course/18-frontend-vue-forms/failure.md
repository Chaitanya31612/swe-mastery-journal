## Break it and reason about the repair

Resetting from props on every server refresh can wipe a dirty draft. Sending the whole entity can include server-owned fields. A stale response can erase a newer edit.

**Remember:** A failed save should lose the request, not the work.

## Break it and reason about the repair

update_all bypasses model callbacks/validations. A callback’s after_commit hook can still lose enqueue during a crash gap.

Removing a callback without tracing callers can remove behavior from an import.

**Remember:** Map the hidden path before moving it.
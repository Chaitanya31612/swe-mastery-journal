## Trace the execution

List entry points and callback registrations. Record one completion with timestamps and event ID.

Add tests for update!, bulk updates, imports, and rollback according to their actual paths.

Then change one caller. Assert one logical event, not merely one method invocation under a fake.

Inspect direct SQL/bulk methods that intentionally bypass callbacks.
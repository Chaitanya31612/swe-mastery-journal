# Follow the execution

Trace PUT /tasks/7: route chooses update; authentication runs; the scoped find either returns an allowed task or raises not found; permitted input reaches update; the action chooses JSON and status.

The private helper cannot be called as a public action. Use request tests for missing authentication, another user’s ID, rejected attributes, validation errors, and a successful update. Also assert the database row stayed unchanged on rejection.

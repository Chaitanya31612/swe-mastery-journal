# Follow the execution

Start with a reported symptom: POST /complete takes 12 seconds. Find the request ID, then time the database step and provider step.

Check whether timeouts and retries explain the total duration. A bigger thread pool may only increase pressure on the slow dependency.

Release a database change in compatible steps when old and new app versions overlap. Keep a rollback path.

A feature flag cannot undo data already deleted. Write a short runbook: symptom, check, safe action, verification.
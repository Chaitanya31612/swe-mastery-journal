## Understand

A longer explanation should have an application run ID and explicit state. Store actor/scope, task identity, source version, prompt/model version and outcome metadata. A job loads that run, rechecks current access, obtains facts, calls the provider, validates the result, and stores an allowed terminal state.

Persisting a run and enqueueing a job are separate boundaries unless the chosen queue/database mechanism unifies them. For important work, use a durable enqueue strategy or an outbox/recovery process. Rails' in-process async adapter is useful for a local demonstration but loses queued work on process exit.

Result access needs its own authorization. A user should not fetch another user's run by guessing its ID. A job started while access was valid may finish after revocation. Recheck the evidence version and current access before displaying stored results.

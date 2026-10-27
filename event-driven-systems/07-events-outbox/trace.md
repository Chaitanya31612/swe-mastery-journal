## Trace the execution

HTTP completion → lock/check → ticket update + outbox insert → DB commit → dispatcher reads → producer delivery acknowledgement → published mark. Break the process at each arrow and state what can be retried.

after_commit enqueue alone still has a crash gap. It can be useful as a wake-up, but a durable scanner/outbox source must recover missing wake-ups.

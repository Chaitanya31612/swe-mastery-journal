## Trace the execution

Choose a question → choose a structure/key → execute a bounded operation → inspect result/TTL → define rebuild or persistence. Compare one command with read-modify-write in application code.

INCR is atomic as that command. GET followed by SET from two clients can lose an update. A string counter also needs a policy for expiry and retry.

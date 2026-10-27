# Follow the execution

A enters the transaction and locks the stock row. B waits for that row. A checks and writes, then commits. B continues and sees the new quantity before deciding. Test with independent connections so the overlap is real.

Callbacks are hidden control flow. A concern can install one when included. Draw callback order and side effects before moving them. A clear use-case method often makes orchestration easier to test.

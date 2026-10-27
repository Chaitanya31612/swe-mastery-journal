## One valid approach

A durable operation still needs a recorded status and idempotency/reconciliation path. The UI can stop rendering, but cancellation must not erase evidence of an effect that may have occurred.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

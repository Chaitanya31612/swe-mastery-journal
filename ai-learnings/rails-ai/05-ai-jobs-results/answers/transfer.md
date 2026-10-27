## One valid approach

Use a durable transaction/enqueue design or a recovery scanner for pending intents with safe claiming. Record explicit pending/failed states. Do not rely on a frontend spinner to infer delivery.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

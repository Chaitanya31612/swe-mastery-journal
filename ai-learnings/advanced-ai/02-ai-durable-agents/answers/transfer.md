## One valid approach

Use a current claim/version/fencing check at the protected state boundary and business idempotency for effects. A lock expiry is not proof the old worker stopped.

Preserve and reconcile uncertain outcomes.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.
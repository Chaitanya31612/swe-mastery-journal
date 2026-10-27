## Follow the execution

Claim step → record intent → execute idempotent/reconcilable action → store observed outcome → checkpoint → resume under current policy. Inject a crash before/after each boundary and inspect whether an effect repeats or a completed action is lost.

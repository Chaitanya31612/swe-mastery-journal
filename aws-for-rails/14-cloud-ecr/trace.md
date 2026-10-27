## Trace the execution

Build → scan/check → push → resolve digest → deploy that artifact → observe → roll back to a known digest if needed. Connect logs/deployment metadata to the source and digest.

Retention rules must not remove every artifact needed for rollback. Large layers and old tags also consume storage; define a deliberate policy.
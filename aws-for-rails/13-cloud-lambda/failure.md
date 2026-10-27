## Break it and reason about the repair

Stateless compute does not mean the business effect is idempotent. Execution environments may be reused, so avoid treating mutable globals as per-user durable state.

**Remember:** Small handler, explicit source contract, bounded downstream work.

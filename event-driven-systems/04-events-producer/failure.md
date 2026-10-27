## Break it and reason about the repair

Fire-and-forget publication can lose errors. Producer idempotence is often overclaimed as exactly-once business processing. App-level resends remain a distinct duplicate source.

**Remember:** Buffer accepted ≠ broker acknowledged ≠ business completed.

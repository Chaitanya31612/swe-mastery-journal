## Break it and reason about the repair

Two replicas can run the same schedule. A local file lock does not necessarily coordinate separate hosts. DST can make a local scheduled time absent or repeated.

**Remember:** Schedule the trigger. Persist the run. Observe completion.

## Trace the execution

Assigned partition → fetch → validate → DB transaction → commit completed progress.

Parallel processing needs a contiguous completion frontier: do not commit past an earlier unfinished record merely because a later one finished.

Test a consumer restart with an existing group and then a new group. Explain the difference from resetting offsets deliberately.
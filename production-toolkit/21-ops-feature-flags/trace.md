## Trace the execution

Request context → flag decision → chosen behavior → observable outcome → guarded expansion → retire old path. Log a bounded variant tag where useful so errors can be compared.

Rehearse disabling the flag after the new path has written data. If the old path cannot read that data, the flag is not an effective rollback.
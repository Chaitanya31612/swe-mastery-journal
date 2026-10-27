## Trace the execution

Configuration + variables + state + provider context → plan → human/team review → apply → refreshed state → observed service. A successful apply proves resources changed, not that Rails works end to end.

Before a replacement/destruction, inspect why the provider proposes it and which data/lifecycles are affected. Keep backups and recovery separate from state-file backups.

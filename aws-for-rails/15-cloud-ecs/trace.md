## Trace the execution

Scheduler starts task → platform pulls image using execution role → app receives workload task role/config → process becomes ready → traffic/work arrives → logs/metrics report progress.

On shutdown, stop accepting new work and finish or safely retry current work.

Count DB pools across every web and worker task before scaling. Managed task placement does not expand PostgreSQL capacity.
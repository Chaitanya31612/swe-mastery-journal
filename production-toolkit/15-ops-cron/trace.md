## Trace the execution

Calendar tick → process environment → command → unique business run → durable work → completion/failure.

On restart after a day of downtime, decide whether the app enumerates missing periods or intentionally skips them.

Test overlap, duplicate scheduler instances, failed exit, and late starts. A log saying command started is not proof a report completed.
## Understand the idea

Logs explain individual events. Metrics summarize trends.

Traces connect steps across boundaries. CloudWatch provides AWS-native observability capabilities; choose the signals and retention you actually need.

An alarm should point to user impact or a meaningful precursor, not merely an interesting chart. “Oldest export age is growing” can be more actionable than queue count alone.

Include scope, threshold/time window, owner, and the first safe checks.

Setup: send structured app/container logs, define bounded metric dimensions, retain data deliberately, add a small dashboard and alarm, then simulate a synthetic failure and follow the runbook.

Do not emit user IDs or event IDs as unbounded metric labels.
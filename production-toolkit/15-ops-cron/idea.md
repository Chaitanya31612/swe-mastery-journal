## Understand the idea

cron evaluates calendar schedules and starts commands in its environment. It does not ensure the previous run finished, that the command succeeded, or that a missed business period is repaired.

Environment variables, working directory, shell, and timezone can differ from your interactive terminal.

Make the logical run explicit: daily-report(workspace, business_date). A unique database key and retry-safe use case protect duplicate triggers.

Decide catch-up behavior after downtime and how DST/local-time rules apply.

For distributed deployments, choose one scheduler ownership strategy or an orchestrator schedule with a documented concurrency/missed-run policy. Still keep business deduplication.

Logs/exit status and oldest expected-run age should reveal silent failures.
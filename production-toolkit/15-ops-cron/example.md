## Follow a concrete example

```cron
# Example: 02:15 in the scheduler's configured timezone.
15 2 * * * /app/bin/run-daily-report
```
The wrapper should set its expected environment, call the application use case, and return an honest exit status. It should not rely on a developer’s current directory or shell profile.
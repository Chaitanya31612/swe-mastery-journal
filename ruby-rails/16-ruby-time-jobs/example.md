## Follow a concrete example

```ruby
# Illustrative key: one daily report per workspace calendar date.
run_key = "daily-report:#{workspace.id}:#{local_date.iso8601}"
# Enforce uniqueness in a ReportRun table, then create delivery intent.
# Time.zone helpers must use the intended workspace zone deliberately.
```
Use a fixed test clock and zones with/without DST. Never use the current host timezone as an accidental business rule.
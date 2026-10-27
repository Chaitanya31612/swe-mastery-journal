## Follow a concrete example

```text
SET learning:ticket:42:summary "open" EX 60
HSET learning:ticket:42 title "Export fails" status open
SADD learning:workspace:7:watchers user-1 user-2
ZADD learning:workspace:7:priority 8 ticket-42
INCR learning:metrics:completed
```
These are Redis command examples for an isolated lab. Observe TYPE, TTL, and expected result.

A wrong-type error is useful feedback about your data model.
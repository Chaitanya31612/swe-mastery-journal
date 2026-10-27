## Trace the execution

App records bounded metric → collector observes → query transforms over a time window → panel/alert presents it → investigator checks user outcome.

A missing scrape and a true zero value are different things.

For a latency claim, ask which requests were included and whether errors/timeouts were excluded. A low median can coexist with painful tail latency.
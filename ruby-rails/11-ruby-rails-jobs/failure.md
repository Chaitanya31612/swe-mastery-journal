# What can go wrong

Testing Sidekiq inline changes timing and can hide a transaction visibility bug. Enqueueing before commit can let a worker read data that is not committed yet.

A cache key without tenant scope can leak another tenant’s result.

**Memory cue:** Later means changed. Retry means repeat.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.
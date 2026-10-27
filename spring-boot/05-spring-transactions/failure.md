# What can go wrong

A unit test using new CompleteTask(...) bypasses the proxy. It can test business decisions but cannot prove transaction interception. A transaction-wrapped test can also hide a missing production boundary.

**Memory cue:** The wrapper must see the call.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

# What can go wrong

await pauses that async function, not the whole browser. A long synchronous loop still blocks input. A stale request can also clear the current loading spinner if only result assignment is guarded.

**Memory cue:** Start order is not finish order.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

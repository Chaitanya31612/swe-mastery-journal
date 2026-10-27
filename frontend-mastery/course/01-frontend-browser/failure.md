# What can go wrong

A new Date() or random value rendered independently on server and client can produce different first markup. Browser-only APIs such as localStorage are not available during server execution.

**Memory cue:** URL → request → tree → layout → paint.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

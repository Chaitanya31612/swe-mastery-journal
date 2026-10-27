# What can go wrong

A singleton service with a field named lastTask is shared state. Marking the field volatile does not make a multi-step business operation atomic. Avoid the field when the value belongs to one call.

**Memory cue:** Share services. Pass request data.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

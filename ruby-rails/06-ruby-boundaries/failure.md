# What can go wrong

Logging the whole settings file may leak secrets. Tests should use synthetic temporary files.

A retry around a non-idempotent side effect can repeat work after a timeout.

**Memory cue:** Catch what you can explain. Test what you can observe.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.
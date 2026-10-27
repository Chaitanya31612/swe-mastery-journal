# What can go wrong

Returning an entity can trigger lazy queries during JSON serialization or reveal an internal field. A 200 response containing {error: ...} also makes clients guess whether the operation succeeded.

**Memory cue:** Bind → check → act → reply.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

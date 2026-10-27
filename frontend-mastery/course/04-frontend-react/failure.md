# What can go wrong

An effect that only computes fullName from firstName/lastName stores redundant state. Derive it during rendering.

React’s scheduling details do not mean any render is allowed to mutate external state.

**Memory cue:** Render reads a snapshot. Updates request the next one.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.
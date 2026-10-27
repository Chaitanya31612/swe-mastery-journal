# What can go wrong

A deep watcher is not free: it can traverse much data. Replacing computed with a watcher can add stale state. In Vue 2, setting list[index] directly has different detection behavior from splice.

**Memory cue:** Read through the reactive link.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

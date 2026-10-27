# What can go wrong

A test marked @Transactional may roll back its own work and hide production commit/after-commit behavior. Verify relevant effects after the actual use-case transaction has completed.

**Memory cue:** Test at the layer where the bug can live.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

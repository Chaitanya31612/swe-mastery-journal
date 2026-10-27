## Break it and reason about the repair

Testing private implementation details makes refactors expensive. Broad snapshots may miss the important failure. Arbitrary sleeps make the test depend on machine speed.

**Remember:** Test the promise the user sees.

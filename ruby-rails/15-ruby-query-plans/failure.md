## Break it and reason about the repair

to_a before filtering moves potentially huge work into Ruby memory. Per-row association reads create N+1.

A batch loop that changes its own selection criteria needs a progress rule.

**Remember:** Count rows, objects, and queries separately.
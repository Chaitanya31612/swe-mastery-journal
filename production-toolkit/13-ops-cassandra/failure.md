## Break it and reason about the repair

A very large/hot partition can dominate one path despite many nodes. ALLOW FILTERING is not a universal performance solution.

Cross-table denormalization can leave inconsistent projections after failure.

**Remember:** Query first. Bound the partition.

Plan the extra copies.
# The idea

An ActiveRecord relation is a description of a query. where, order, and limit can build it. Iteration often executes it. Once you call to_a, later filtering is usually Ruby work over loaded rows.

Associations can issue queries too. A list of tasks followed by task.owner.name can create one extra query for each task. Preloading brings the required owners in a bounded set of queries. includes may choose different SQL strategies depending on how the relation is used. Inspect the actual SQL instead of assuming a fixed count.

For large lists, choose a stable order and bounded pages. pluck reads selected column values without building full model objects. find_each batches records but has version-specific ordering behavior; do not use it when its order conflicts with a user-facing sequence.

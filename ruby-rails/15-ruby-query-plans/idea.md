## Understand the idea

A report can be correct on ten rows and fail on a million.

Ask how many rows are loaded, how many model objects are built, how many queries run, and whether the order matters.

Use SQL filtering/aggregation when it expresses the required rule. Use pluck for selected values when full model behavior is unnecessary.

Use batches for large iteration, but check the Rails version’s batching order and limits. Rails 4.2 APIs differ from modern cursor options.

An index serves an actual predicate and order. Check the plan on representative synthetic PostgreSQL data.

Avoid assuming an index is used merely because it exists. A large export may need a stable snapshot/job contract rather than paginating a moving live list.
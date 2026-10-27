# One valid repair

Push the filter, order, and limit into SQL: Task.where(done: false).order(:id).limit(20).preload(:owner). Measure rows returned and query count.

Use selected fields or pluck when objects are unnecessary. Test page ordering and missing owners according to the association contract.

**How to check:** Relations commonly build query descriptions until a result-consuming operation needs rows.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
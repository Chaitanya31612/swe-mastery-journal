# Data access, caches, and atomic boundaries — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. Two instances claim the last item. Which mechanism targets the race?
   - A. Check Redis then update later
   - B. Atomic authoritative conditional claim
   - C. Lock a local variable in one instance
   - D. Add a read replica

2. Deleting a cached value after a write proves what?
   - A. Universal linearizability
   - B. The source can never be stale
   - C. Nothing about all concurrent repopulation without further assumptions
   - D. No need for a freshness contract

3. A transaction updates local rows then calls an external provider. Which statement is sound?
   - A. Both systems are automatically atomic
   - B. Retries cannot duplicate the external effect
   - C. Serializable isolation covers remote HTTP
   - D. Remote uncertainty needs an explicit protocol/cooperation

4. Which pattern should drive initial database selection?
   - A. Required queries, invariants, and operations
   - B. Popularity alone
   - C. A universal writes/s threshold
   - D. Avoiding all schemas


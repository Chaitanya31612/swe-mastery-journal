# Distributed key-value stores and honest consistency claims — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. R+W>N establishes which basic fact for fixed designated sets?
   - A. All possible operations are linearizable
   - B. Read/write sets overlap
   - C. Clocks cannot skew
   - D. Membership is safe

2. A write acknowledged only in volatile memory guarantees what under power loss?
   - A. Permanent durability
   - B. Three backups
   - C. Not durable persistence by itself
   - D. Automatic repair

3. Concurrent profile versions are detected. What remains?
   - A. Nothing
   - B. Ignore all versions
   - C. Use hashing as a merge
   - D. A domain conflict/merge policy

4. Why keep backups when replicas exist?
   - A. Deletion/corruption can propagate to replicas
   - B. Replicas never store data
   - C. Backups are low-latency caches
   - D. They replace every failover mechanism


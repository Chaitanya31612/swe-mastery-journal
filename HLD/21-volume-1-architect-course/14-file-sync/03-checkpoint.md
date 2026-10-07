# File sync: versioned metadata and recoverable conflicts — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. A stale editor must not silently overwrite. Which mechanism targets that?
   - A. Longer filenames
   - B. More notifications
   - C. A public CDN
   - D. Expected-version conditional publication

2. Notifications are lost. What can still recover sync?
   - A. Durable change log and catch-up cursor
   - B. Socket status alone
   - C. Path string alone
   - D. Cache hit rate

3. When is orphan collection safe?
   - A. Immediately after upload starts
   - B. After reference/session checks and a suitable safety policy
   - C. Whenever a notification times out
   - D. Before metadata commits

4. Content hashes alone establish which property?
   - A. All authorization
   - B. No concurrent metadata conflict
   - C. A candidate content identity/integrity mechanism under assumptions
   - D. Unlimited retention


# Production practice: service objectives, security, and safe evolution — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. Which is the most user-relevant async-work SLI?
   - A. Only queue server uptime
   - B. Only CPU average
   - C. Time until eligible accepted work completes
   - D. Only process count

2. Why can unlimited retries worsen an outage?
   - A. They remove workload
   - B. They make every call idempotent
   - C. They prove provider failure
   - D. They amplify load and consume resources

3. A backup’s existence proves what?
   - A. Not that restore meets RPO/RTO without testing
   - B. All data is current
   - C. Failover is instantaneous
   - D. Deleted data is never replicated

4. What must accompany schema cutover?
   - A. Deleting old fields immediately
   - B. Compatibility, verification, and a valid rollback plan
   - C. Assuming dual writes never diverge
   - D. Only a new diagram


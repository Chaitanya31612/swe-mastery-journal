# Requests, scale, and useful estimates — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. 400 requests/s and stable mean residence time 0.5 s imply what?
   - A. About 200 in-flight requests on average
   - B. Exactly 200 CPU cores required
   - C. Exactly 400 database connections
   - D. No queueing

2. CPU is low but latency is high. Which next step is strongest?
   - A. Buy more CPU immediately
   - B. Trace wait time and dependency/pool saturation
   - C. Ignore it because low CPU proves spare capacity
   - D. Shard all tables

3. What determines cache RAM most directly?
   - A. Daily response bytes alone
   - B. Number of application routes
   - C. Distinct cached objects, sizes, overhead, and locality
   - D. Employee count

4. A sustained producer rate exceeds consumer capacity. What follows?
   - A. A larger queue fixes the deficit forever
   - B. Average CPU alone proves recovery
   - C. Retries reduce arrivals automatically
   - D. Backlog grows unless capacity, admission, or work changes


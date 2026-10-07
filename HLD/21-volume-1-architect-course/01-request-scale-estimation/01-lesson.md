# Requests, scale, and useful estimates

Learning outcome: Trace a request, separate latency from throughput, estimate capacity with units, and choose a bottleneck from evidence.

## The request is a sequence of work and waits

A client resolves a name, establishes/reuses a connection, negotiates TLS where needed, sends a request, and waits for application/dependency work. DNS, a reverse proxy, a CDN, and a load balancer perform different jobs; a small service need not have each as a separately operated component. A CDN serves cacheable content near users. A load balancer distributes traffic among healthy backends. A reverse proxy can route and enforce policies. Trace the actual path instead of drawing every possible layer.

Latency is duration per operation; throughput is completed operations per unit time. Low CPU does not establish low latency: connection-pool wait, locks, disk, network, or a slow dependency can consume time. Averages hide tails. An end-to-end percentile is not generally the sum of per-stage percentiles; correlated delays and distributions matter. For diagnosis, separate queue time from service time and correlate traces with saturation metrics.

## Derive the numbers that change the design

`average operations/s = active users/day × operations/user/day ÷ 86,400`. Choose a peak factor explicitly. `stored bytes = new objects/day × retention days × mean bytes/object`; indexes, replication, metadata, and temporary processing add capacity. `bandwidth = delivered objects/s × mean bytes/object`; multiply bytes/s by eight to get bits/s. Label decimal GB versus binary GiB.

In a stable system, Little’s Law links average in-flight work to arrival rate and mean residence time: `L = λW`. At 200 requests/s and mean 0.25 seconds in the system, about 50 requests are in flight. This is not an exact worker-sizing rule under overload or variable service times. A queue can absorb a short burst; if λ exceeds sustainable service capacity indefinitely, backlog grows.

## Scale the actual scarce resource

Stateless application instances allow horizontal distribution, but database connections, hot rows, and external quotas can remain shared limits. Vertical scaling may be simpler before partitioning. Persistent user/session state needs a deliberate store/routing strategy, not accidental process memory. Autoscaling needs a useful signal, lead time, capacity ceiling, and protection during warm-up.

Before changing architecture, measure a suspected bottleneck. Adding application replicas when the database connection pool is saturated may increase contention. A faster query/index or bounded concurrency may help more. For availability, identify what happens when an instance/store fails and where useful service continues. Replicas are not a substitute for restoration from accidental deletion.

## Explain the decision

State the load estimate, the limit it suggests, the supporting metric, and the simplest intervention. Avoid universal SQL/NoSQL or shard-at-QPS rules. Historical latency numbers in the book illustrate orders of magnitude; measured contemporary hardware/workloads determine deployment capacity.

## Retrieve before practicing

Explain why scaling an API can harm a shared database. Recompute P1 when each view makes only one DB read and page bytes triple.

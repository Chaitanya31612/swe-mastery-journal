## Understand

The cost of a feature can include embeddings, retrieval/reranking, input/output/reasoning usage, retries, multi-step tools, storage, and operator review. Measure cost per accepted task at the required quality.

Current prices vary, so use configuration and actual usage rather than memorizing course numbers.

Separate latency stages and distributions. A fast median can hide a slow tail.

Concurrent long requests can exhaust worker threads, DB connections, queue capacity or provider quotas. Use backpressure, concurrency limits, deadlines and tenant/user budgets with an explicit over-limit state.

Optimize from evidence. Reduce irrelevant context, avoid unnecessary steps, cache under correct authority/version boundaries, route tasks deliberately and use asynchronous work when the user benefit permits it.

Always compare the quality regression risk and fallback behavior.
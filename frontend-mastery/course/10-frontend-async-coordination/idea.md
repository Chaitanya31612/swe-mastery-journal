## Understand the idea

await describes a dependency: the next line waits for that promise in this function. Two awaits in sequence may waste time when their inputs are independent. Promise.all waits for all successes but rejects when one rejects; it does not automatically cancel the others. allSettled preserves each outcome when partial results are useful.

Cancellation and acceptance are different. AbortController can stop a supported fetch. A request number or active flag says whether a result may still update this screen. Guard error and loading state as well as rows.

Parallel does not mean unlimited. Launching 10,000 uploads at once can exhaust memory and connections. Use a bounded worker pool or a queue. Retry only a safe operation and only within a deliberate attempt/time limit.

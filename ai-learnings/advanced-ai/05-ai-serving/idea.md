## Understand

Managed APIs reduce serving operations but add external dependency, capability, region and data-handling choices. Self-hosting gives different control and responsibilities: model artifacts/licensing, hardware, serving runtime, security, updates, capacity, evaluation and recovery.

“Open weights” does not automatically mean unrestricted use or production readiness.

Model weights occupy memory. Serving also needs KV cache, activations, runtime overhead and concurrency capacity.

Quantization represents some values with fewer bits and can reduce memory/compute costs under a chosen implementation, with quality and compatibility tradeoffs.

A smaller weight file does not by itself predict full serving memory or acceptable latency.

Prefill/decode, batching, scheduling and cache management affect user latency and throughput. More batching can improve throughput while increasing queue delay.

Compare actual task quality and end-to-end latency on representative context lengths and concurrency. Reasoning-heavy calls may spend output/compute budget that a short visible answer does not reveal.
## One valid approach

Measure full runtime memory across representative context/output lengths and concurrency, including KV cache and overhead. Compare throughput, tail latency, quality regressions and cost.

Define backpressure and an overload fallback.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.
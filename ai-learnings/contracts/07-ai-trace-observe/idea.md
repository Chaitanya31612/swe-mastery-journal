## Understand

A useful trace shows task, run ID, prompt/model versions, retrieval version, tool calls, validation decisions, fallback reason, durations, token usage, and outcome. It does not require storing every raw conversation or document.

Separate operational telemetry from a deliberately reviewed evaluation dataset. Minimize inputs, redact where appropriate, restrict access, and define retention.

A hash is useful for correlation in some cases, but is not automatically anonymous or safe for low-entropy sensitive values.

Break end-to-end latency into retrieval, queueing, provider time, tool work, and validation. Track accepted answers and meaningful task outcomes, not only request success.

A 200 response with an unsupported explanation is still a product failure. Cost accounting should include retries and multi-step work.
## One valid approach

Choose one owner for provider transport retries, cap total attempts and elapsed time, and record attempt counts. Let durable job orchestration distinguish safe retryable steps from uncertain effects. Use jitter and concurrency limits. Preserve a no-model fallback.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

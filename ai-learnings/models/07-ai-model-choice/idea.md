## Understand

Start with the operation: classify intent, extract fields, explain supplied facts, retrieve text, inspect an image, or coordinate tools. These may need different model capabilities. An embedding model produces vectors; a generation model produces outputs. A reranker scores query–candidate relevance. They are not interchangeable.

Compare useful quality at an acceptable failure rate, latency, cost, context limit, modality, structured-output/tool support, region, and data-handling constraints. Pricing and model names change, so the course uses configuration placeholders rather than hardcoded “best” choices.

A larger or reasoning-heavy model can help a hard task but also add latency and budget. A small model can work well on a narrow typed task. Start with a measured baseline, then route only cases that justify extra work. A framework or provider switch should preserve the application contract, not hide capability differences.

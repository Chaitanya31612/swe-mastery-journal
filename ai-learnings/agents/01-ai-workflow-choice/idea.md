## Understand

A workflow follows code-defined paths. An agentic loop lets a model propose some next steps or tools based on observations. The distinction is who chooses the next operation, not whether the product has a chat box.

Many useful features are workflows: classify request → validate filter → fetch facts → explain. Fixed paths are easier to test, budget, and reason about. An agent becomes useful when the necessary sequence depends on what it discovers, such as inspecting several permitted sources before forming a comparison.

Use the simplest path that meets the task. Adding autonomy adds possible tool sequences, latency, cost, and failure modes. The host must still enforce capabilities, budgets and stopping. A framework can help orchestration but cannot decide your product's trust model for you.

## Understand

An agent can reach a correct answer through an unsafe path. Another can fail one tool gracefully and still give a useful partial result. Evaluate the trajectory: requested tools, argument validity, policy decisions, evidence, stopping reason, effects, cost and latency.

Use scripted tools and deterministic fault injection to test runtime behavior. Use actual model runs on representative held-out tasks to assess planning/tool choice. Keep those two claims separate. A scripted agent passing tests does not establish that a live model will choose the right tool.

Create adversarial tasks: a document asks to call an unrelated tool, a name is ambiguous, a permission is revoked mid-run, a tool hangs, a write outcome is unknown, or a model loops. Define acceptable partial results and disallowed operations before judging.

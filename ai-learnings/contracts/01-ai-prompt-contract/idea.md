## Understand

A prompt is an input contract for a probabilistic component. State the task, allowed evidence, output shape, ambiguity behavior, and limits. Prefer concrete examples over a long list of vague demands such as “be accurate.” Version the prompt alongside the code that validates its output.

Keep trusted application instructions separate from user text, documents, and tool results. Role or delimiter structure helps communicate that boundary; it is not a complete security sandbox. A malicious instruction inside a retrieved page remains outside data even if it sounds authoritative.

Few-shot examples demonstrate valid behavior. Include a normal case, an ambiguous case, and an unknown case. Avoid examples that silently grant access or teach unsupported default values. Test changes on cases that were not used to write the examples.

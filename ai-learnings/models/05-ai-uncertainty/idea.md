## Understand

A model can make unsupported statements, invent sources, or combine real facts into a wrong conclusion. These failures are often called hallucinations.

The useful engineering question is specific: which claim lacks evidence, and what check can catch it?

A statement such as “I am 95% confident” is generated text unless tied to a defined, validated measurement.

Token probabilities measure likelihood under a model and context; they are not automatically calibrated probabilities that a business answer is correct.

Give the system explicit unknown and ambiguous states. “I found two depots with that name” is better than silently choosing one.

A citation identifies a source; checking that the source ID exists does not prove the claim follows from it. Combine structural checks, deterministic checks where possible, and task-level evaluation.
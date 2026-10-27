## Understand

Dispatch Desk is a fictional warehouse operations assistant. It can propose shipment filters, explain a blocked shipment, compare a small selection, and summarize grouped blockers. It is one worked example in this general course, not the definition of AI integration.

Keep model work narrow. Code authenticates, resolves names, filters records, verifies hold rules, counts/group rows, and determines permitted navigation. The model interprets language and drafts explanations using supplied facts. The first version is read-only: a suggested next step is not an executed change.

Use ordinary Rails layers. A controller authenticates and validates request size. A use-case service coordinates work. Provider adapters isolate model formats. Policies/scoped relations control data. Jobs handle longer work. Result validators and presenters keep UI labels honest. Each layer has a focused test.

## Trace the execution

Trace the same assignment from HTTP and a background import. Both must enforce the core transition rule. Then replace only the remote receipt adapter with a fake and test the use-case result.

For a new requirement, identify which boundary changes. A new HTTP representation need not rewrite the domain rule. A new provider should mostly change an adapter if its semantics fit the existing contract.

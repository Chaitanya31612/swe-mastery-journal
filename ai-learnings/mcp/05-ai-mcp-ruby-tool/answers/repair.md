## One valid approach

Remove actor identity from arguments. Bind the actor in trusted server context and use a domain service that scopes the lookup. Test direct service access and SDK invocation using a foreign ID. Return a generic unavailable result where appropriate.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

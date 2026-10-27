## One valid approach

Store approval per operation with argument digest, actor, target, scope, version and expiry. Revalidate at execution and require a new approval for changes. Use an application-owned stable operation identity for retries and record outcome.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

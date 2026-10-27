## One valid approach

No. Transport/API scope and record-level authorization are independent. The domain service must reject the lookup under the actor’s current tenant and permission policy.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

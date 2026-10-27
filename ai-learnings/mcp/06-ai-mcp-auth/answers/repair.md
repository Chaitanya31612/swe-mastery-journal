## One valid approach

Restrict destinations and use credentials intended for each resource. Validate upstream audience/scope and map a trusted principal.

Apply downstream authorization deliberately. Do not allow arbitrary model-selected egress or token passthrough.

Test wrong-resource tokens and redirects.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.
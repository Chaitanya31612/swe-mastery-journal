## One valid approach

Remove identity/privilege arguments. Bind them in the host, expose only the required lookup/filter fields, and enforce scoped access and field projection in code. Add negative tests for valid-shaped forbidden IDs and permission changes.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

## One valid approach

Bind actor context per authenticated request/connection according to the supported SDK lifecycle, with no shared mutable user state. Keep tool lookups scoped and reauthorize on execution. Test interleaved requests from two tenants.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

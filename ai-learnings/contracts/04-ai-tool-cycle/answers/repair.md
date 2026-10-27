## One valid approach

Replace dynamic dispatch with an explicit tool registry. Validate each schema and permission, enforce per-call/run budgets, and normalize unknown tool names. Keep reads separate from writes. Test an unsupported name, foreign ID, oversized output, and a loop that never finishes.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

## One valid approach

Set bounded tool output sizes and total run budgets. Keep structured state separately; select relevant history and evidence for each step. Preserve tool-call/result pairs and stop with an honest partial result when the budget is exhausted.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

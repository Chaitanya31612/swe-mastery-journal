## One valid approach

Key artifacts by source/version/parser/chunking/embedding identity, make inserts/upserts idempotent, and publish only a complete validated revision. Test a mid-job crash and retry.

Keep deletion/retention behavior explicit.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.
## One valid approach

Keep statuses in the authoritative DB and expose scoped reads. Retrieve durable documents separately. Test a status change between two requests and verify that the second answer uses current facts. Fine-tuning is not a live-data synchronization protocol.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition. Do not award yourself a passing check for naming a tool.

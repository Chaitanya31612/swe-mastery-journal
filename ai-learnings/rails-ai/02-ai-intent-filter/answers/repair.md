## One valid approach

Reject tenant_id and every unsupported field. Bind tenant through Shipment.visible_to(actor), then apply only validated status/depot conditions.

Assert that the rejected proposal cannot influence the SQL scope or provider evidence.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.
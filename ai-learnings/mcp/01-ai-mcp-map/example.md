## Walk through an example

Dispatch Desk can host a model. Its MCP client connects to a read-only warehouse capability server. The model proposes read_shipment_facts. The host validates the proposal, the client calls the server, and the server performs its own actor-scoped lookup.

The server can also be called by another approved host. That reuse is the interoperability benefit.

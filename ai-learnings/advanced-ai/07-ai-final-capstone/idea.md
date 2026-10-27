## Understand

Design a vendor-support workbench. Users can ask for filtered tickets, explain why a ticket is waiting, compare a small selection, and ask questions over approved support policies.

Live ticket fields and counts come from current scoped queries. Document answers need permitted versioned evidence.

A read-only MCP server exposes a narrow facts capability.

## Constraints to test

- two tenants
- one actor can lose access while a job is running
- the same depot/vendor name can be ambiguous
- one policy revision conflicts with another
- a document contains an injected export instruction
- a provider can time out
- the UI must work at narrow widths
- a run has a four-tool-step budget.

The feature remains useful without generation.

Begin with a threat/data-flow sketch and a deterministic baseline. Implement a vertical slice, then add retrieval and a bounded tool loop only where justified.

Keep generated interpretation labels honest. A passing quiz is preparation for this demonstration, not a substitute for it.
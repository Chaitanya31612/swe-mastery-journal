## Understand

A tool grants a possible capability to the host application, not an entitlement to every requested resource. Choose names and schemas that describe a specific operation.

Read_shipment_facts is easier to constrain than run_query or execute_code.

Bind the actor, tenant, role and request purpose outside model-supplied arguments. Validate IDs through current scoped data.

Recheck access at execution time, because a tool proposal can outlive the permission or record version it was based on.

Keep tools read-only until a product requirement justifies writes. Even read tools can reveal sensitive information or cause external effects, such as fetching a URL that logs access.

Restrict egress, output size, query cost and result fields. Tool annotations/descriptions are useful metadata; they do not enforce behavior.
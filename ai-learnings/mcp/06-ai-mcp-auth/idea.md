## Understand

For HTTP-based remote MCP, the selected specification defines an authorization framework using protected-resource metadata and authorization-server discovery.

Use a supported OAuth flow for the deployment rather than inventing a token exchange inside a tool.

Validate token issuer, audience, expiry and scopes through appropriate middleware/libraries. Do not forward an upstream access token to a downstream service that was not its intended audience.

Token passthrough and confused-deputy behavior can give a caller powers it should not have.

An access token that permits calling read_shipment_facts still does not authorize every shipment. Resolve the principal and apply tenant/record/field policy at the domain boundary.

Bind identities per request. Session IDs and resource URIs are not authentication credentials.

The local lab uses synthetic demo identity and is explicitly not a production OAuth implementation.
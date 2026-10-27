## Walk through an example

A local training host can spawn a Ruby MCP server with only the environment variables it needs. A Rails deployment can place an authenticated Rack boundary before the SDK HTTP transport.

Do not put a shared mutable current_user in a global server object. Pass request-local trusted context or use a supported request-aware integration.
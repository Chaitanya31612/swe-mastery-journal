## Understand

Stdio commonly connects a host to a locally launched server process. Protocol messages share standard input/output; logs should not corrupt that channel.

“Local” does not mean harmless: the process has OS permissions and access to its inherited environment.

Streamable HTTP connects over HTTP using the selected MCP transport rules, which may include JSON responses or server-sent events. Sessions, protocol-version headers, reconnection, origin handling and proxy behavior matter.

It is not merely a generic POST route that accepts tool names.

Use the SDK transport for its supported revision and test through the actual reverse-proxy/runtime path. Remote identity and authorization are separate from the transport's ability to deliver messages.

A stateless server still needs a current authenticated actor for every operation.
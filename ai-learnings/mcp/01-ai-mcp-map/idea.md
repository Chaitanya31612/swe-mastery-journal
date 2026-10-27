## Understand

Model Context Protocol standardizes how an AI application connects to tools and context providers. The host is the application coordinating the experience. A client connection inside the host talks to an MCP server. The server exposes capabilities such as tools, resources, and prompts. The model is a separate participant in the host's overall workflow.

A provider function call and an MCP tool call are not the same wire message. The host can translate between its model provider's tool proposal and an MCP client's request. It must still decide which tools to expose, which result data may enter context, and whether an operation is authorized.

MCP does not train a model, provide RAG by itself, or grant database permissions. It is useful when several hosts need a standard interface to the same capabilities. A single Rails service can begin with an ordinary internal interface; use MCP where interoperability adds value.

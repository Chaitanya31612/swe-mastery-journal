# Think of MCP as a shared way to connect tools

**Model Context Protocol (MCP)** lets an AI application talk to tools and sources through a common protocol.

It helps you reuse a connection format. It does not decide who may read your data.

## Three parts to picture

```text
Host application
    ├── talks to the model provider
    └── contains an MCP client ↔ MCP server ↔ allowed tools and data
```

- **Host:** the app that manages the experience and decides what the model can use.
- **Client:** a connection inside that host that sends and receives MCP messages.
- **Server:** exposes tools, resources, or prompts through MCP.

These roles do not have to be separate deployed services.

## A small example

The model suggests reading a parcel’s facts.

The host checks the proposal. Its MCP client calls a tool on the shipment server.

The server checks the current user’s access before returning facts.

The provider’s tool-call message and the MCP message are different formats. The host can translate between them.

## When to use it

MCP is useful when several hosts need the same tool interface.

For one internal Rails feature, a small ordinary service interface may be enough to start.

## Remember

MCP connects capabilities. Your application still owns permissions, validation, and execution limits.

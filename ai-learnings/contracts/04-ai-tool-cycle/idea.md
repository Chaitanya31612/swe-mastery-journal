## Understand

The model can emit a request to use a declared tool. In a client-side integration, your host application receives that proposal, validates it, executes permitted code, and returns a tool result. The model does not obtain the function's privileges merely by generating its name.

A tool definition describes name, purpose, and argument shape. Keep descriptions narrow and schemas small. Resolve identity outside arguments. Treat arguments as outside input and results as potentially untrusted content. Return bounded data with explicit errors.

The host maintains the conversation item linking a call ID to its result. A second model step can use the result to answer or propose another call. Put limits on steps, time, output size, and total cost. Some platforms can execute tools server-side; their execution boundary and authorization still need an explicit design.

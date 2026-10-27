## Understand the idea

Nginx can accept HTTP traffic and proxy it to application servers, serve suitable static content, and enforce selected request/timeout rules. It is not a database pool or application permission layer.

Managed ALB/CDN choices may cover some needs differently.

PgBouncer pools PostgreSQL connections. Its pooling mode changes how long a client is associated with a server connection.

Transaction pooling can conflict with assumptions about session state or certain prepared-statement/client behaviors unless the selected versions/configuration support them.

Add either tool for a measured boundary. A proxy timeout, app timeout, and provider timeout should form a coherent budget.

A pool should protect capacity, not hide long transactions forever. Verify Rails/pg compatibility with the chosen mode in a separate test environment.
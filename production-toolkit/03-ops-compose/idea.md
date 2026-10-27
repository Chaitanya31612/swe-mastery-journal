## Understand the idea

Compose describes a multi-container application. Services can reach one another by service name on their configured network. localhost inside a container refers to that container, not the database next door or your host browser.

Published host ports and container service ports are different. The browser may use localhost:3300 while the worker uses web:3000. Kafka also advertises broker addresses to clients, so correct bootstrap reachability alone is not enough.

depends_on ordering is not universal application readiness. Use health checks/conditions where supported and keep client startup/retry behavior deliberate. Name volumes and project scope so a lab does not collide with another application. Read the cleanup command before removing any volume.

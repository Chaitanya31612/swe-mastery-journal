## Understand the idea

ECS orchestrates tasks and services. A task definition describes containers, resources, ports, configuration, and roles.

A service maintains a desired task count. Fargate is a capacity option that removes much of the host management; it does not remove application or network responsibility.

Use the same image with different process commands for web and workers when that fits the app.

Scale them from their own signals: request pressure for web, backlog/age and safe concurrency for workers.

A DB migration is a deliberate one-off task, not an action every new replica should race to run.

Setup: push an image to ECR, create execution/task roles, define task resources and commands, choose private networking/egress, wire logs and secrets, attach web targets to ALB, configure health/graceful shutdown, then run a smoke path and a worker failure.
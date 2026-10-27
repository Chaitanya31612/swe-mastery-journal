## Understand the idea

A VPC is a network boundary you configure. A subnet belongs to one Availability Zone. A route table decides where traffic goes. A security group controls allowed traffic for attached resources; a route and a permission rule solve different parts of connectivity.

“Private subnet” does not mean an application has no outbound needs. A worker may need S3, a queue, image registry, or an external email API. NAT and VPC endpoints are different ways to reach services, with different scope and costs. Choose the path you need; do not add a NAT gateway by reflex.

Setup sketch: choose non-overlapping CIDRs, subnets in two zones, explicit route tables, an internet-facing load balancer where needed, private app/database placement, and security-group references that allow only the intended paths. Record DNS resolution and outbound service access.

## Trace the execution

A request needs DNS, a routable destination, a listener, and allowed traffic. A database timeout is not the same as a database login rejection.

Follow the packet one hop at a time.

For S3 from a private task, inspect the endpoint/NAT route, endpoint policy, task IAM role, and bucket policy. Network reachability does not imply S3 authorization.
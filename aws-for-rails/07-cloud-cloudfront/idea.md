## Understand the idea

CloudFront is an edge delivery/cache layer in front of an origin. Static versioned assets are a natural fit. Dynamic or personalized responses require a deliberate cache key and authorization policy.

Cache identity answers which requests may share a response. If two users receive different data but the key omits that difference, a shared cache can leak content. Do not solve this by forwarding every header blindly; that can destroy cache usefulness and complicate origin behavior.

Setup: select an origin, restrict direct S3 origin access when appropriate, create behaviors for assets versus dynamic paths, choose cache/origin-request policies, configure TLS/domain, and test hit/miss plus a private-user boundary. Version asset names to avoid expensive broad invalidations for every release.

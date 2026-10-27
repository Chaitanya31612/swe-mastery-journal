## Trace the execution

Resolver asks DNS → caches an answer → browser connects to that destination → TLS verifies hostname/certificate → HTTP request begins. A certificate error is different from NXDOMAIN or a target timeout.

For cutover, plan existing cache lifetimes, overlapping service readiness, rollback, and certificate coverage. DNS is one part of the release, not the whole release mechanism.
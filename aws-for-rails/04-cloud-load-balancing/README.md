# 4. Application Load Balancer: traffic is a separate layer

**Beginner · about 2 hours with practice**

Configure listeners, target health, and request routing without confusing liveness with readiness.

## Use it

Public Rails traffic and rolling deployments.

**Benefit:** Central traffic routing and health-based distribution.

**Cost or limit:** Proxy headers, timeouts, and health contracts need configuration.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [ALB introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)

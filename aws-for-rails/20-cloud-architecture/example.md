## Follow a concrete example

```text
Route 53 + ACM → ALB → Rails web (ECS or EKS)
                           → RDS PostgreSQL
                           → ElastiCache for a defined cache role
Browser ↔ authorized S3 upload/download; CloudFront for deliberate delivery
Rails outbox → dispatcher → MSK/Kafka → reporting consumer → projection
Report request → SQS/worker → S3 result
All paths → request/event identity → CloudWatch/Datadog telemetry
Workload roles + Secrets Manager/KMS across explicit boundaries
```
Draw ECS and EKS as alternatives in your decision sketch, not a mandatory chain.
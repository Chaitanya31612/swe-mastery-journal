# AWS · Run a Rails application

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [AWS identity: accounts, roles, and the caller you actually are](01-cloud-identity/README.md): Set up a training identity and distinguish human sign-in, workload roles, trust, and permissions.
- 02. [VPC networking: follow the packet](02-cloud-networking/README.md): Trace public ingress, private application traffic, database access, and outbound AWS calls.
- 03. [EC2 and EBS: when you own the machine](03-cloud-ec2/README.md): Explain instance lifecycle, disk persistence, process supervision, and the responsibilities EC2 leaves with you.
- 04. [Application Load Balancer: traffic is a separate layer](04-cloud-load-balancing/README.md): Configure listeners, target health, and request routing without confusing liveness with readiness.
- 05. [Route 53 and ACM: names and trust before the request](05-cloud-dns-tls/README.md): Explain DNS records, certificate validation, region constraints, and what a DNS change does not instantly control.
- 06. [SNS: fan out one fact to independent subscribers](11-cloud-sns/README.md): Distinguish publish/subscribe fan-out from competing workers on a queue.
- 07. [Lambda event functions: small work with explicit retry boundaries](13-cloud-lambda/README.md): Choose an event-function boundary and handle retry, concurrency, and database pressure.
- 08. [ECR: publish an artifact you can identify and replace](14-cloud-ecr/README.md): Explain image tags, digests, registry access, scan results, and release retention.
- 09. [CloudWatch: logs, metrics, alarms, and a useful runbook](18-cloud-cloudwatch/README.md): Connect an application symptom to a metric, trace/log identity, alarm, and recovery check.

## Intermediate

- 10. [S3 for Rails attachments: private objects and signed access](06-cloud-s3/README.md): Set up private object storage and trace metadata, upload, authorization, and download separately.
- 11. [CloudFront: fast delivery without mixing private users](07-cloud-cloudfront/README.md): Choose cache keys, origin access, and freshness rules for assets and authorized downloads.
- 12. [RDS PostgreSQL: managed database, owned data model](08-cloud-rds/README.md): Configure private connectivity, backups, failover expectations, and Rails connection limits.
- 13. [ElastiCache: choose managed cache and queue roles deliberately](09-cloud-elasticache/README.md): Separate cache data from durable work and plan client behavior during eviction or failover.
- 14. [SQS: work delivery, visibility, and deletion](10-cloud-sqs/README.md): Set up a queue and dead-letter path and implement repeat-safe processing.
- 15. [EventBridge: route integration events by meaning](12-cloud-eventbridge/README.md): Configure an explicit event bus/rule/target contract and debug a missing delivery.
- 16. [ECS with Fargate: web and workers as separate services](15-cloud-ecs/README.md): Configure task definitions, roles, networking, logs, health, and scaling for Rails web and worker processes.
- 17. [EKS: Kubernetes control plane does not operate your application](16-cloud-eks/README.md): Choose EKS for a concrete Kubernetes need and map AWS responsibility versus cluster/workload responsibility.
- 18. [MSK: managed Kafka still needs event design](17-cloud-msk/README.md): Map broker management, clients, network, identity, partitions, and consumer operations in AWS.
- 19. [Secrets Manager and KMS: credentials and encryption keys are different](19-cloud-secrets-kms/README.md): Deliver secrets and authorize key use without confusing encryption with application access.
- 20. [A complete Rails application on AWS: trace four journeys](20-cloud-architecture/README.md): Explain the request, attachment, background job, and event paths, including cost and recovery choices.

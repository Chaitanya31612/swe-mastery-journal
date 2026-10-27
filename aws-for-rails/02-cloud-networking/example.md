## Follow a concrete example

```text
Internet → public ALB :443
ALB security group → Rails task security group :3000
Rails task security group → RDS security group :5432
Rails → S3 endpoint or deliberate outbound path
Worker → permitted provider endpoint
```
This is a design/configuration checklist. Verify the chosen endpoint, DNS, routes, and group rules in your training account before running a workload.
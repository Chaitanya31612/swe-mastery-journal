## Follow a concrete example

```text
EC2 process responsibility map
OS/service manager → starts and restarts Rails/Puma
Instance role → AWS API permissions
EBS → deliberate filesystem persistence
RDS → relational source of truth
S3 → shared attachment objects
```
For a demo, document what is lost if the instance is terminated and which volume deletion settings apply. Do not infer persistence from one reboot.
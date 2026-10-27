## Understand the idea

RDS manages parts of database infrastructure, not your schema, query design, or business rules. You still choose engine/version, instance/storage settings, network, credentials, backup retention, maintenance, and application connection behavior.

High availability and read scaling are different goals. A standby/failover arrangement is not automatically the same thing as an application read replica. Read replicas can lag; sending a read-after-write there can show old data. Use the selected RDS deployment type’s exact contract.

Setup: choose a training PostgreSQL engine/version, private subnet group and DB security group, credential delivery, backup/restore policy, connection settings, and monitoring. Test connection failure and a restore to a separate instance with synthetic data. A backup checkbox is not a completed recovery exercise.

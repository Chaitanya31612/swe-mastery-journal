# 8. cron and scheduled work: a trigger is not a transaction

**Beginner · about 2 hours with practice**

Read a schedule and design missed-run, overlap, timezone, and deduplication behavior.

## Use it

Reports, reminders, and periodic repair/reconciliation.

**Benefit:** Simple calendar triggering.

**Cost or limit:** Overlap, downtime, environment, and business success remain separate.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [POSIX crontab](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html)
- [Kubernetes CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

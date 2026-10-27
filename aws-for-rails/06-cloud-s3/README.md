# 10. S3 for Rails attachments: private objects and signed access

**Intermediate · about 2 hours with practice**

Set up private object storage and trace metadata, upload, authorization, and download separately.

## Use it

Private attachments and generated reports.

**Benefit:** Shared durable object storage without app-local upload disks.

**Cost or limit:** Metadata consistency, URL lifetime, lifecycle, and transfer costs need design.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [S3 guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [Presigned access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)

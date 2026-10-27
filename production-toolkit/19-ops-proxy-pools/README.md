# 20. Nginx and PgBouncer: two different kinds of front door

**Intermediate · about 2 hours with practice**

Distinguish HTTP reverse proxying from database connection pooling and test their compatibility limits.

## Use it

Understanding existing reverse-proxy and DB pool deployments.

**Benefit:** Traffic control and connection reuse where appropriate.

**Cost or limit:** Timeout/buffering/session contracts can change behavior.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Nginx proxy guide](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [PgBouncer features](https://www.pgbouncer.org/features.html)

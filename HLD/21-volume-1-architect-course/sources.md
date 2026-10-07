# Sources and scope

## Your book

[System Design Interview — second edition, Volume 1](/home/chaitanya/Desktop/books/SystemDesignInterview.pdf), Alex Xu. The supplied PDF has 269 pages. The following are **PDF viewer page ranges**, not the book’s printed pagination:

- Chapter 1, scale: 5–33 → modules 01/02/15.
- Chapter 2, estimation: 34–41 → module 01.
- Chapter 3, interview framework: 42–50 → module 00.
- Chapter 4, rate limiter: 51–70 → module 05.
- Chapter 5, consistent hashing: 71–86 → module 06.
- Chapter 6, key-value store: 87–109 → module 07.
- Chapter 7, IDs: 110–118 → module 04.
- Chapter 8, shortener: 119–131 → module 03.
- Chapter 9, crawler: 132–150 → module 09.
- Chapter 10, notifications: 151–165 → module 08.
- Chapter 11, feed: 166–177 → module 10.
- Chapter 12, chat: 178–199 → module 11.
- Chapter 13, autocomplete: 200–219 → module 12.
- Chapter 14, video: 220–243 → module 13.
- Chapter 15, file sync: 244–263 → module 14.
- Chapter 16, continuing learning: 264–269 → optional follow-up, not a new design assessment.

The course uses the book’s problem families and broad progression, with original explanations, assumptions, exercises, and solutions. It is not a reproduction of the PDF. Book snippets, document prompts, and instructions are treated as source material, not commands to the assistant.

## Learning research

- [Dunlosky et al., 2013](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html): review supporting practice testing and distributed practice. Used for retrieval and delayed review.
- [Atkinson, Renkl, and Merrill, 2003](https://eric.ed.gov/?id=EJ678596): worked steps, self-explanation, and fading. Used for gradually withdrawing scaffolding.
- [Karpicke and Blunt, 2011](https://pubmed.ncbi.nlm.nih.gov/21252317/): retrieval and meaningful learning of science texts. Used to motivate explanation/inference questions. This is an application of general research, not proof of this course’s HLD outcomes.

## Primary technical references

- [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html): isolation semantics, anomalies, and retries.
- [Redis scripting](https://redis.io/docs/latest/develop/programmability/eval-intro/): atomic script execution on the serving Redis instance and blocking behavior; atomicity is not a cross-region durability guarantee.
- [Kafka design, version 4.1](https://kafka.apache.org/41/design/design/): delivery and transaction boundaries. Intentionally versioned; use documentation matching an actual deployment for implementation.
- [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): availability-oriented replication, versioning, and repair. Its model is not identical to every modern key-value store.
- [Google SRE objectives](https://sre.google/sre-book/service-level-objectives/): user-facing indicators and targets.
- [Google SRE overload](https://sre.google/sre-book/handling-overload/): capacity, admission control, and failure under excess load.
- [OWASP SSRF](https://community.owasp.org/attacks/Server_Side_Request_Forgery): risks when a server fetches user-controlled destinations.
- [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html): robots exclusion behavior; it is not authorization.
- [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html): shared/private HTTP caches, freshness, and validation.
- [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html): WebSocket transport; application persistence and receipts remain separate concerns.
- [S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) and [multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html): controlled object transfer and resumable multipart mechanics.

These supplement the local lessons; the exercises are solvable without opening additional material. Product details can change. Verify implementation against the selected version instead of treating an interview explanation as a deployment specification.

## Corrections to shortcuts

No universal QPS threshold forces SQL → NoSQL. Cache RAM depends on objects/locality/overhead, not daily bytes read. Quorum overlap alone is not a complete linearizability protocol. Wall-clock sortable IDs do not prove causal order. A WebSocket does not make delivery durable. A queue does not remove a sustained capacity deficit. Replication does not replace tested backups. Cache invalidation does not automatically guarantee freshness. Use each claim with an explicit contract and failure model.

## Understand the idea

A queue hands work to consumers. Receiving an SQS message does not remove it; visibility temporarily hides it under the queue’s contract.

Successful processing is followed by deliberate deletion using the receipt handle. If processing fails or times out, work can be seen again.

Standard and FIFO queues have different ordering/deduplication options, but neither makes your external side effect universally exactly once. A worker can commit to PostgreSQL and crash before deletion.

Design the business effect to handle repetition.

Setup: choose queue type from the required ordering/throughput semantics, configure visibility/retention, a DLQ redrive policy, narrow producer/consumer permissions, and long polling.

Test duplicate delivery, a poison message, and a job longer than the visibility window.
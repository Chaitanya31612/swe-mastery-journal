## Understand the idea

SNS can publish a message to subscriptions. This is fan-out: independent destinations can receive the same published fact. A set of workers competing on one queue instead shares work among them. Choose based on whether each downstream system needs its own copy.

Use SNS-to-SQS when subscribers need their own buffering and processing pace. Define message schema, subscription filtering, access policies, and failure/retry handling. Delivery behavior depends on topic and subscription types; record the exact option rather than assuming one global ordering guarantee.

Setup: create a training topic, create a separate queue for each durable subscriber role, add subscriptions/filters, allow only the intended topic to send to each queue, then publish a synthetic event and verify each required subscriber independently.

## Trace the execution

Create one synthetic ticket. Complete it twice: the business transition should create one logical completion event.

Wait for reporting: one inbox/effect appears. Re-publish the saved envelope: Kafka can contain another record with the same event_id, while the local projection effect remains one.

Stop the dispatcher before completion, then restart it. Saved intent should still be found.

Stop the consumer, publish, then restart it. Retained history and group progress should let it catch up within retention.
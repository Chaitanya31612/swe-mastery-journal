# Async workflows, retries, and notification delivery — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Multi-provider notifications

An order service produces five million notifications/day with 10× peaks. Provider A permits 300 sends/s; provider B permits 200/s. Users have channel preferences, and duplicates are undesirable. Design acceptance, outbox/dispatch, retries, failover between providers, quotas, expiry, and recovery of unknown outcomes.

## P2 — Report generation transfer

Adapt the workflow to generating a large report then storing it for download. Define a stable job identity, object publication, retries, and the state visible to users. What is different from sending email?

## P3 — Fix bad pseudocode

```text
db.commit_order(order)
queue.publish(order.id)
# worker
send_email(order)
queue.ack()
```

Trace a crash between local commit and publish, then after sending but before acknowledgment. Repair both and state any remaining guarantee limitation.

## Delayed gate

Trace a commit/publish crash and a provider timeout. Explain which duplicates you can prevent locally and which require remote cooperation.

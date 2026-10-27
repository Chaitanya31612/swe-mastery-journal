# One valid adaptation

Persist an outbox event with the business change in the same transaction. A scanner finds undispatched rows and retries.

Make consumers tolerate duplicates because dispatch and acknowledgement can fail independently. after_commit alone does not save pending delivery intent.

**Explain back:** One rule. One boundary.

One failure timeline. What changed in the new condition?

What would make your answer fail?
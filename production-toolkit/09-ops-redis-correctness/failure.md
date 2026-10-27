## Break it and reason about the repair

Atomic commands do not make external effects atomic. Pipeline success is not a database commit.

A lock release can delete another owner’s lock if token ownership is not checked.

**Remember:** Atomic here is not atomic everywhere. A lease can expire.
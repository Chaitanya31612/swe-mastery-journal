## Break it and reason about the repair

A set’s uniqueness does not coordinate a PostgreSQL write automatically. A key with no expiry can grow forever. Pub/Sub messages can be missed by disconnected subscribers under its contract.

**Remember:** Ask the query, then choose the structure.

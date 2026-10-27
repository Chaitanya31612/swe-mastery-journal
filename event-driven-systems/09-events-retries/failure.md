## Break it and reason about the repair

Retry topics can break per-key ordering if not designed for it. A DLQ can become a graveyard. More workers do not solve a deterministic poison message.

**Remember:** Every retry design is also an ordering design.

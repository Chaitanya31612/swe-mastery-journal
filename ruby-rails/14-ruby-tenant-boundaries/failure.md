## Break it and reason about the repair

A global find followed by a client-supplied workspace ID can authorize the wrong row. Reusing an unscoped cached object can bypass the intended query boundary.

**Remember:** Carry the scope through every boundary.

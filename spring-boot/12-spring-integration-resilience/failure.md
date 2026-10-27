## Break it and reason about the repair

Nested retries multiply attempts. A 3-attempt client inside a 3-attempt job can make nine calls. A fallback that reports success without performing the required effect is a false result.

**Remember:** Bound the wait. Identify the command. Admit uncertainty.

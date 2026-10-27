## Break it and reason about the repair

Using localhost for db from web points at the wrong container. Removing volumes erases local lab data. A started DB process may still be initializing or lack the schema.

**Remember:** Know which network the client is standing in.

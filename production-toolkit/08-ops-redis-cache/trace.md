## Trace the execution

Read miss → DB load → cache fill. Now interleave a write: A reads old DB, B commits new DB and deletes cache, A fills old value. A simple “delete after write” rule can still have a stale-fill race.

Choose a consistency policy that matches the requirement: tolerate bounded staleness, version entries, use guarded refresh, or read the authority for strict decisions. Test the chosen timeline.

## Follow a concrete example

```text
Release rehearsal
1. Start old app against synthetic database.
2. Apply compatible schema expansion once.
3. Start new app and verify critical paths.
4. Simulate provider slowdown and one denied action.
5. Stop new app; verify old app still reads the expanded schema.
6. Record data effects that a code rollback does not reverse.
```
Do not let every app replica independently run a risky long backfill on startup.
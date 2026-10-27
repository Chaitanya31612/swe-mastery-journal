# Follow the execution

Two transactions can both pass a uniqueness validator before either inserts. The unique index makes only one conflicting insert succeed. The losing code must handle the database error and return a useful result.

For a rename, use expand → backfill → switch reads/writes → remove old data later. Verify both versions work during deployment. Test the migration on a disposable database with old-shaped data.

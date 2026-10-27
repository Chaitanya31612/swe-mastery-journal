## Trace the execution

PR event → least-privilege test job → passing evidence → identified artifact → deliberate environment gate → deployment → smoke/monitor → rollback decision. Keep credentials scoped to jobs/environments that need them.

Treat migration compatibility and external effects as release concerns. A green CI job cannot make a destructive data rollback reversible.
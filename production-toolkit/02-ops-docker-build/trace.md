## Trace the execution

Build context → dependency layers → app layer → runtime command → registry digest. Change only a source file and inspect which layers rebuild.

Then change a gem lock and predict the invalidation.

During stop, SIGTERM should reach the process so it can stop taking work and finish or abandon it safely within the orchestrator’s grace period.
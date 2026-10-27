## Trace the execution

Boot image → inject configuration/identity → start supervised process → health check → receive traffic.

Replacement should recreate the application from its artifact/configuration, not depend on manual edits left on the old machine.

Scale to two instances and follow an upload/read. If only one instance has the file, the storage boundary is wrong for that architecture.
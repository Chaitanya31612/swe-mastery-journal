## Trace the execution

Application emits structured entry → event service accepts/rejects that entry → pattern matches → permitted target receives → consumer handles business effect. Debug one hop at a time with event/request identity.

If no target event appears, check producer entry result, bus/region/account, pattern field spelling/type, target permission, delivery retry/DLQ state, and consumer state.

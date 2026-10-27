## Trace the execution

User-visible latency spike → service latency/error metrics → slow trace → SQL or provider span → correlated safe logs → hypothesis → controlled repair → monitor recovery. Async boundaries need explicit context propagation/linking rather than assuming one synchronous stack.

An absent trace can mean sampling or missing instrumentation, not proof the request never ran.

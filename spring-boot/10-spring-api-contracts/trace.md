## Trace the execution

A creates a ticket and commits, but the response is lost. A retry with the same key reads the saved result rather than creating a second ticket.

A different payload with that key receives a deliberate conflict.

Test simultaneous same-key requests, a timeout after commit, an invalid cursor, and permission changes. Define key retention; forgetting keys eventually changes retry behavior.
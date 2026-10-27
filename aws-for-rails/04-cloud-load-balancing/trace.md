## Trace the execution

Client connects → TLS listener → routing rule → healthy target → Rails → response. On a 502/503/504, identify whether there were no healthy targets, a connection/protocol issue, or a slow target/dependency.

During deployment, allow draining and graceful shutdown so an old target can finish appropriate in-flight work before termination.

## Understand the idea

Datadog combines observability capabilities such as infrastructure monitoring, APM, logs, and monitors. Choose the signals needed for a concrete investigation. Installing an agent alone does not make every request/job trace connected.

Use stable service, environment, and version tags. Instrument the relevant Rails/client/job libraries with versions supported by your runtime. Current datadog gem setup differs from legacy ddtrace setups; a Rails 4.2/Ruby 2.7 application needs a verified compatibility choice.

Setup path: choose supported tracer/agent versions, configure a training service identity and agent path, instrument a request and worker, correlate logs safely, define a useful monitor/runbook, and verify with a synthetic slow dependency. Review sampling, sensitive fields, ingestion, retention, and billing dimensions.

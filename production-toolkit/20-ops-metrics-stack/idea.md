## Understand the idea

Prometheus commonly scrapes exposed metrics and stores time series. Grafana can query/display data from selected sources. A dashboard is a view over a data contract, not an independent guarantee that the service is healthy.

Counters accumulate events; rates describe change over time. Gauges describe a current value. Histograms can help examine latency distributions under their configuration. Choose labels with bounded categories. A ticket ID per metric label can create an enormous number of series.

Setup: define one task-relevant metric, expose it safely in a training service, configure a scrape, create a query/panel, and trigger a synthetic failure. Then write an alert with an owner and runbook. Consider hosted alternatives or Datadog when their operating model fits better; using both stacks is not mandatory.

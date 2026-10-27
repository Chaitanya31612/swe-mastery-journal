## Follow a concrete example

```yaml
startupProbe:
  httpGet: {path: /live, port: 3000}
  failureThreshold: 30
  periodSeconds: 2
readinessProbe:
  httpGet: {path: /ready, port: 3000}
livenessProbe:
  httpGet: {path: /live, port: 3000}
resources:
  requests: {cpu: "100m", memory: "256Mi"}
  limits: {memory: "512Mi"}
```

Illustrative values only: measure the actual Rails startup, memory, and traffic. Do not paste arbitrary limits into production.

## Follow a concrete example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: tickets-web}
spec:
  replicas: 2
  selector: {matchLabels: {app: tickets-web}}
  template:
    metadata: {labels: {app: tickets-web}}
    spec:
      containers:
        - name: web
          image: learning/tickets:chosen-version
          ports: [{containerPort: 3000}]
```
This manifest fragment needs a real image, configuration, resource policy, and probes. It is not automatically applied to any cluster.
## Follow a concrete example

```yaml
apiVersion: v1
kind: Service
metadata: {name: tickets-web}
spec:
  selector: {app: tickets-web}
  ports:
    - port: 80
      targetPort: 3000
```
```sh
kubectl get pods -l app=tickets-web
kubectl get service tickets-web
kubectl get endpointslices -l kubernetes.io/service-name=tickets-web
```
Run only against a deliberately selected training context/namespace.
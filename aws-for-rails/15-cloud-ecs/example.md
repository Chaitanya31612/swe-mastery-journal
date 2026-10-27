## Follow a concrete example

```text
Task definition tickets-web: image@digest, command bundle exec puma
Task definition tickets-worker: same image, deliberate worker command
Web service → ALB target group
Worker service → queue and DB permissions
One-off release task → compatible migration
```
Do not copy a web health probe onto a worker that does not run HTTP. Define worker health from progress and process behavior.
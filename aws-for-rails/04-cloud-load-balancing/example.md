## Follow a concrete example

```text
Listener :443 → target group tickets-web
Target port :3000
Health path /ready
Healthy means: this instance can accept the intended traffic now.
```
Keep /live as a narrower process-health concept if you need it. Do not make every unrelated external provider failure trigger a restart loop.
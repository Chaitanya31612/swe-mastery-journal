## Follow a concrete example

```yaml
services:
  web:
    build: .
    ports: ["127.0.0.1:3300:3000"]
    environment:
      DATABASE_URL: postgres://learning:learning-only@db:5432/tickets
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: learning
      POSTGRES_PASSWORD: learning-only
      POSTGRES_DB: tickets
```

This small fragment omits persistence/health to make those decisions visible. Use the complete event lab for the tested setup; credentials here are synthetic local training values.

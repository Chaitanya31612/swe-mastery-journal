# A small example

```properties
# Teaching defaults. Expose only the endpoints you actually need.
management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=never
spring.jpa.open-in-view=false
```

Capstone: build POST /tasks, GET /tasks/{id}, and POST /tasks/{id}/complete in the sandbox. Use request DTOs, a service, persistence, ownership, tests, and a fake notification boundary. Read the SQL count for the list endpoint. Add one failure at a time.

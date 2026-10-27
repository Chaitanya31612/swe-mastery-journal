## Follow a concrete example

```yaml
# Rails database.yml concept; values arrive from the training environment.
production:
  adapter: postgresql
  host: <%= ENV.fetch('DB_HOST') %>
  database: <%= ENV.fetch('DB_NAME') %>
  username: <%= ENV.fetch('DB_USER') %>
  password: <%= ENV.fetch('DB_PASSWORD') %>
  pool: <%= ENV.fetch('DB_POOL', '5') %>
```

Configure TLS/certificate verification according to your pg/client and RDS setup. Do not log the rendered connection credentials.

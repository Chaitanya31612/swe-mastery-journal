## Follow a concrete example

```ruby
require 'aws-sdk-secretsmanager'
client = Aws::SecretsManager::Client.new(region: ENV.fetch('AWS_REGION'))
response = client.get_secret_value(secret_id: ENV.fetch('DB_SECRET_ID'))
config = JSON.parse(response.secret_string)
# Validate expected fields. Never print config.
```

Retrieving on every request is usually unnecessary. Cache/refresh under a deliberate lifetime and failure policy; account for workload restarts when secrets are injected only at startup.

## Walk through an example

```ruby
client = OpenAI::Client.new(api_key: ENV.fetch('OPENAI_API_KEY'), max_retries: 0)
response = client.responses.create(
  model: ENV.fetch('AI_MODEL'), store: false,
  input: [{role: :user, content: 'Classify this synthetic request.'}],
  text: {format: {type: :json_schema, name: 'intent', strict: true, schema: schema}},
  request_options: {timeout: 8}
)
# Inspect completion/refusal state, parse output, then validate domain meaning.
```

Optional provider example; no API key is needed for the offline lab. A schema variable and business parser are defined in its files. Model and SDK compatibility must be checked before an online call.

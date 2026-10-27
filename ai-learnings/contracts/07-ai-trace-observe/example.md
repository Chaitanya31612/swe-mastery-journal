## Walk through an example

```ruby
logger.info({event: 'ai_run_finished', run_id: run.id,
  prompt_version: 'filter-v1', validation: 'accepted',
  fallback: false, duration_ms: elapsed_ms}.to_json)
```

This example deliberately omits user text, credentials, retrieved documents, and generated prose. Add only fields that answer a real debugging question.

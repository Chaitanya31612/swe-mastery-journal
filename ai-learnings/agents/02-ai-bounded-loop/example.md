## Walk through an example

```ruby
MAX_STEPS.times do
  proposal = model.next_step(context)
  return validate_answer(proposal) if proposal.final?
  call = registry.validate!(proposal)
  policy.authorize!(actor, call)
  observation = registry.execute(call, actor: actor)
  context = append_bounded_result(context, call.id, observation)
end
Result.partial(reason: 'step_limit', evidence: collected_facts)
```

The local lab uses scripted proposals so tests can reproduce every transition. Scripted behavior is not evidence of live model quality.

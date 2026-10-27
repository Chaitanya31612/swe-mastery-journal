## Understand

An AI integration has several changing dependencies: model snapshot/alias, prompt, schema, tools, retrieval corpus/index, rules, SDK, policy and UI. A change to any can alter behavior. Record the effective combination and run regression checks before enabling it broadly.

Shadow mode can run a candidate without letting its output control user-visible behavior. It still consumes data and budget, so use approved inputs and explicit limits. A limited cohort rollout should have success/failure thresholds, monitoring and a rollback owner. Compare practical task outcomes, not only a provider uptime chart.

During an incident, identify the affected versions and boundary. Disable optional generation or a specific capability while deterministic work continues. Preserve minimal diagnostic evidence, reconcile uncertain effects, and turn a reviewed reproduction into a new regression case.

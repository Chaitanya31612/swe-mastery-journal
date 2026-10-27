## Build a support workbench from a blank page

A vendor-support team handles tickets for two customer organizations. They need to find waiting tickets, explain a delay, compare up to five tickets, and read approved support policies. The first release is read-only.

### Your constraints

- Identity comes from the application. The model must never choose an organization or actor.
- Exact counts and waiting reasons come from current records and reviewed rules.
- Policy documents can be revised, withdrawn, or contain hostile instructions.
- A user can lose access after a job is queued. A ticket can change before its answer is opened.
- A provider may time out, refuse, produce malformed output, invent a citation, or request an unknown tool.
- Runs have at most four tool steps. The UI must still offer a useful manual path.

### Submit these artifacts

1. A Task → Truth → Boundary → Flow → Failure → Measure design. State one feature you deliberately keep deterministic.
2. One architecture diagram and one sequence diagram for a delayed answer.
3. A file map for controller, policy/scopes, facts, provider, validator, run/job, presenter, MCP tool and tests. Give each file one responsibility.
4. One running vertical slice. Use a synthetic provider first. A copied folder with renamed classes is not sufficient: add a new waiting reason or requirement and prove the change.
5. A labelled evaluation set. Include normal, ambiguous, missing-evidence, hostile, stale and unauthorized cases. Keep a held-out subset.
6. Evidence for at least four negative checks. Capture the actual provider input at a fake adapter so you can assert forbidden facts are absent. Do not log real private payloads.
7. A release decision with cost/latency limits, rollback conditions, unknowns, and a no-model path.

Use Predict, Change, Verify, Explain in your submission. Quote actual command results only if you ran them. For a design-only attempt, identify exactly which checks remain unverified. Submit before opening the reference.

# Build one useful Rails feature

Dispatch Desk is a fictional assistant for a warehouse team.

It is one worked example in this course. The same boundaries apply in other domains.

## Four small tasks

- Suggest filters for a list of shipments.
- Explain a shipment’s current hold reason.
- Compare a small selection.
- Summarize grouped hold reasons.

The first release only reads data. A suggested action does not change a shipment.

## Follow one request

```text
Controller → current user and access checks → use-case service
                                             ↓
                                  current facts and reviewed rules
                                             ↓
                                  optional model call → result checks → UI
```

Code owns names, filters, rules, counts, and allowed links.

The model interprets language and drafts explanations using the supplied facts.

## Give each file one job

A controller checks identity and input size. A service coordinates the use case.

A provider adapter handles the model API. Policies and scoped queries decide what data is allowed.

A job handles longer work. Validators check results. A presenter gives facts and generated text clear labels.

Test each boundary separately.

## Remember

An AI feature still needs ordinary, understandable application code.

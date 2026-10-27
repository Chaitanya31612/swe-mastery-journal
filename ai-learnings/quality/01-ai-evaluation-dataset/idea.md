# Compare what you expected with what happened

That is the core of an **evaluation**.

Start with the job the feature must do. Then choose checks that show whether it did that job.

## A small example

```text
Input:    “Held parcels at East”
Problem:  two depots match that name
Expected: ask which depot
Wrong:    guess one and show a confident answer
```

For a filter, check the allowed fields and unclear requests.

For an explanation, check the facts and whether they support the claims.

For an agent, also check tool choices and execution limits.

## Build a useful set of cases

Include normal requests, unclear requests, missing evidence, and known failures.

Use synthetic data. Label valid alternatives rather than requiring one exact sentence.

Keep some cases out of prompt development. This **held-out set** gives you a less rehearsed release check.

## An average can hide the problem

A high score is not reassuring if the system fails every access-control case.

Report results by failure type. Treat forbidden data or actions as release blockers under your agreed rules.

Record the model, prompt, index, and tool versions so you know what you compared.

## Remember

Measure the decision you care about. Do not let a good average hide a serious failure.

# Follow the execution

For eight ordered candidate changes, binary search can often narrow the culprit with only a few checks. The exact sequence follows commit ancestry, not wall-clock guesses.

If the first bad commit is a dependency update, that identifies a trigger, not the whole root cause. Reproduce the behavior and explain why the change activates it. Keep the regression test after the investigation.

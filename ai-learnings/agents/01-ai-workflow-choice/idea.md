# Who chooses the next step?

In a **workflow**, code chooses the path.

In an **agent loop**, the model can suggest a next step based on what it finds.

## Start with a workflow

```text
Understand request → check filter → fetch facts → draft explanation → validate
```

Code already knows these steps. A workflow is usually easier to test and limit.

A chat box does not automatically make the system an agent.

## When a loop may help

Suppose the task needs several sources. The model may need to inspect one result before choosing the next useful source.

That can justify a loop. It does not justify unlimited access or unlimited retries.

## Keep the application in charge

Limit tools, steps, time, and spending.

Check every proposed operation before running it. Stop with a useful partial result when a limit is reached.

A framework can coordinate steps. It cannot choose the application’s trust rules for you.

## Remember

Use fixed steps when the path is known. Add model-chosen steps only when they help the task.

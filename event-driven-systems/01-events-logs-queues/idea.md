# Start with a command and an event

A **command** asks for work: `GenerateReport`.

An **event** says something happened: `TicketCompleted`.

The difference helps you decide who can reject work and who owns the next step.

## Two delivery models

```text
Work queue:    job → one of the available workers
Retained log:  saved events → independent readers with their own positions
```

A queue commonly shares jobs among workers.

A retained log keeps ordered records for a configured time. Each consumer group tracks how far it has read.

## When Kafka helps

Two teams may need the same events for different purposes. One builds reports; another sends notifications.

Independent subscribers and replay can make a retained log useful here.

A background job alone is not a reason to add Kafka. A direct call or your existing job queue may be enough.

## What changes for the user?

Work may finish later. Show a useful pending state and a way to see the result.

Also plan for duplicate delivery, changing event formats, old permissions, and recovery after failure.

## Remember

Sending work later buys flexibility. It also creates new questions about timing and recovery.

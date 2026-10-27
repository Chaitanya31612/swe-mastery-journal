# A small example

```java
@org.springframework.stereotype.Service
class CompleteTask {
  private final TaskRepository tasks;
  CompleteTask(TaskRepository tasks) { this.tasks = tasks; }
  @org.springframework.transaction.annotation.Transactional
  public void run(long id) {
    Task task = tasks.findById(id).orElseThrow();
    task.title = "done"; // Example managed-field change.
    // Writing a separate outbox row here can make delivery intent atomic.
    // A later worker sends the external message with an idempotency key.
  }
}
```
Call run through an injected CompleteTask bean. For inventory, prefer an atomic conditional SQL update such as UPDATE stock SET quantity=quantity-1 WHERE id=?

AND quantity>0. Check the affected-row count.
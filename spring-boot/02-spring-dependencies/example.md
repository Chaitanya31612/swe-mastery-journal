# A small example

```java
interface Notifier { void send(String text); }
@org.springframework.stereotype.Component
class ConsoleNotifier implements Notifier {
  public void send(String text) { System.out.println(text); }
}
@org.springframework.stereotype.Service
class TaskService {
  private final Notifier notifier;
  TaskService(Notifier notifier) { this.notifier = notifier; }
  void complete(long taskId) {
    notifier.send("Completed " + taskId);
  }
}
```
Test without Spring: new TaskService(text -> captured.add(text)).complete(7). Use an in-memory list owned by that test only.
# A small example

```java
record CreateTask(
  @jakarta.validation.constraints.NotBlank String title) {}
record TaskView(long id, String title) {}

@org.springframework.web.bind.annotation.RestController
class TasksController {
  private final TaskCreator creator;
  TasksController(TaskCreator creator) { this.creator = creator; }
  @org.springframework.web.bind.annotation.PostMapping("/tasks")
  org.springframework.http.ResponseEntity<TaskView> create(
    @jakarta.validation.Valid
    @org.springframework.web.bind.annotation.RequestBody CreateTask input) {
    TaskView task = creator.create(input.title());
    return org.springframework.http.ResponseEntity
      .created(java.net.URI.create("/tasks/" + task.id())).body(task);
  }
}
// TaskCreator is the service boundary; see the runnable sandbox.
```
The validation starter must be installed. @Valid without a validation provider is not a substitute for the dependency.
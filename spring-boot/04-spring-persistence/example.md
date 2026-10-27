# A small example

```java
@jakarta.persistence.Entity
class Task {
  @jakarta.persistence.Id
  @jakarta.persistence.GeneratedValue
  Long id;
  String title;
  @jakarta.persistence.ManyToOne(fetch = jakarta.persistence.FetchType.LAZY)
  Owner owner;
  protected Task() {}
}
// Owner is a separate entity with an id and name.
interface TaskRepository extends
    org.springframework.data.jpa.repository.JpaRepository<Task, Long> {
  @org.springframework.data.jpa.repository.Query(
    "select t from Task t join fetch t.owner where t.id > :after")
  java.util.List<Task> pageWithOwners(@org.springframework.data.repository.query.Param("after") long after);
}
```

This query illustrates a to-one fetch join. It is not a bounded production page: add a limit/Pageable and an explicit order before serving large lists. Collection fetch joins with pagination need special care.

# A small example

```java
import static org.junit.jupiter.api.Assertions.*;
class AccessTest {
  @org.junit.jupiter.api.Test
  void a_different_owner_cannot_edit() {
    TaskAccess access = new TaskAccess();
    assertThrows(org.springframework.security.access.AccessDeniedException.class,
      () -> access.requireOwner(3, 9));
  }
}
```

For HTTP use MockMvc with the appropriate Boot test configuration. For a full HTTP smoke test use @SpringBootTest(webEnvironment = RANDOM_PORT). Boot 4 moved several test annotations to new packages: use the pinned sample and matching reference docs rather than pasting old imports.

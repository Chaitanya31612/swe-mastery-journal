# A small example

```java
// A framework-independent ownership rule, easy to unit test.
class TaskAccess {
  void requireOwner(long callerId, long ownerId) {
    if (callerId != ownerId) throw new org.springframework.security.access.AccessDeniedException("Forbidden");
  }
}
// In a use case: derive callerId from trusted authentication,
// load the task, check ownership, then change it.
// Never take callerId from an editable JSON field as proof of identity.
```
Configure a SecurityFilterChain bean for routes and authentication. This fragment deliberately does not pretend to be a complete production login system.

In the sandbox, test a denied request as carefully as an allowed one.
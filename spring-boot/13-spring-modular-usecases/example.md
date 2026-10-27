## Follow a concrete example

```text
ticket/http/AssignController.java   parse + response mapping
ticket/application/AssignTicket.java  trusted actor + transaction
ticket/domain/AssignmentPolicy.java   allowed transition
ticket/persistence/TaskRepository.java SQL access
ticket/integration/ReceiptGateway.java remote boundary
```

Keep module dependencies one-way. Do not expose every entity field as a public API just to save a DTO.

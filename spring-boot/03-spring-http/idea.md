# The idea

An HTTP endpoint is a boundary. Treat incoming strings and JSON as untrusted input.

Binding turns JSON into Java values. Validation checks those values.

Authorization checks whether this caller may perform this action. These are separate steps.

Keep controller methods short. Convert input, call a use case, then map its result to an HTTP response.

Put reusable business rules in the service. Return DTOs, which are small request/response types, rather than exposing database entities and all their fields.

Choose errors that help the client: bad input is different from a missing record or a conflict. Do not return stack traces or SQL text to callers.

An exception handler can make the error shape consistent.
## Understand

JSON mode asks for JSON. Structured output can constrain a supported model to a supported JSON Schema.

These are different guarantees. Valid syntax and schema adherence still do not prove that a depot exists, a citation supports a claim, or an operation is allowed.

Treat the model response as outside input. Handle refusal, incomplete output, provider error, schema failure, semantic failure, and accepted result as separate states.

Avoid parsing with eval or silently accepting extra fields. Bound string lengths and collections before they reach expensive application work.

Use required fields and explicit enums for supported decisions. A status such as needs_clarification is useful data.

Keep unknown or missing separate from a false or zero value. Your Rails service should return a domain result rather than handing a raw provider object to every controller.
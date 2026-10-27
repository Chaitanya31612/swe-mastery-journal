# One valid repair

Validate a request DTO before service work. Return a TaskView with only allowed fields and 201 on creation.

Test invalid JSON and blank input yield 400 with no creation; missing resources yield 404; conflicts use a deliberate 409 mapping. Validate service rules too when called outside HTTP.

**How to check:** A service can have more than one caller. Its required business rules cannot depend only on controller validation.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
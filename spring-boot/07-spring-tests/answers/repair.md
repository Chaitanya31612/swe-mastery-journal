# One valid repair

Add a database unique constraint on the true key and a test with two independent transactions attempting that key. Assert one stored row and a deliberate conflict response.

A validator pre-check alone races. A Mockito verify call does not test the database rule.

**How to check:** The constraint exists at the database boundary. Test where that rule is enforced.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
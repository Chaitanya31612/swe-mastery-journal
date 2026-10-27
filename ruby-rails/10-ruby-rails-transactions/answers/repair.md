# One valid repair

Use bang writes or explicitly raise/rollback on false. Validate the stock rule under a suitable lock or atomic update.

Assert that a stock failure leaves no reservation. Ensure the failure is not swallowed inside the transaction.

Test the final database state after the boundary.

**How to check:** A false validation result is ordinary control flow unless the caller turns it into a rollback or exception.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
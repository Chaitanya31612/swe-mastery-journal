# One valid repair

The internal call does not cross the usual Spring proxy.

Put the public use-case transaction on the externally called bean method, or move reservation into another injected bean with a public transaction boundary.

Verify actual rollback with a context/database test after the call ends.

**How to check:** The injected bean reference normally points to the wrapper. A self-call stays on the same target object.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
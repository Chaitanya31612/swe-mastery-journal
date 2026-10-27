# One valid repair

An older request can finish while the newest is pending and hide its spinner. Guard loading/error/finally state with the same latest-request identity. Abort obsolete requests when useful, and test old-success/new-success plus old-error/new-success orderings.

**How to check:** The browser drains queued microtasks before choosing the next task. This does not promise order between unrelated network responses.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

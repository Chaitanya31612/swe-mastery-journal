# One valid repair

Call A stores Alice and waits. B stores Bob. A resumes and reads Bob. Pass user as a local argument into each step; remove the shared field. Test concurrent calls with a controlled barrier, not Thread.sleep guesses.

**How to check:** One context can reuse one service across request threads. Scope does not provide locking or distributed coordination.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

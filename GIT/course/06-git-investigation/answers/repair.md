# One valid repair

Replace the network dependency with a deterministic local reproduction of the observed failure. Verify the check repeatedly on known-good and known-bad commits.

Mark untestable commits as skip. Then rerun bisect and inspect the candidate patch.

**How to check:** Bisect depends on the correctness and repeatability of its classification check.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
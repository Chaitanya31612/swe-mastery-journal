# One valid repair

Inspect reflog, show the candidate commit, then create a rescue branch at its ID. Compare/cherry-pick deliberately in a clean context after preserving active changes.

Reflog recovery depends on the object still existing locally.

**How to check:** It records local ref movements and can identify still-existing commits. It does not store arbitrary unsaved files.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
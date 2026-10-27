# One valid repair

Use a stable task ID as the key. Index identity followed position, so React reused a row instance for a different task. Test edit-then-delete/reorder. Keep draft ownership explicit if rows can leave the visible list.

**How to check:** Functional updaters compose with other pending state updates instead of closing over one old value.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

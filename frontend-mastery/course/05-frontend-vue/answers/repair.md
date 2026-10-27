# One valid repair

Return refs, use toRefs on the reactive object, or keep reading state.count through the original object. A computed getter can also preserve the dependency.

Test an update after destructuring; do not only test initial values.

**How to check:** Computed values are for derivation. Watchers/effects are for deliberate side effects.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
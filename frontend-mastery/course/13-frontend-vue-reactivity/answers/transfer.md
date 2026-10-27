## One valid transfer

Keep the external instance outside deep reactivity or use shallowRef/markRaw deliberately. Replace the reactive reference when the UI must notice a new instance. Document which internal changes are not tracked and clean up the instance on unmount.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.

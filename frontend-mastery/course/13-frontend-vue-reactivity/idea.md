## Understand the idea

reactive returns a proxy. Vue can track property reads through that proxy and notify effects when relevant writes happen. ref creates a reactive value wrapper. JavaScript uses .value; templates unwrap refs in supported contexts.

computed should calculate a value from tracked sources. Keep it free of network calls and mutations of unrelated state. watch is for a deliberate side effect. A destructured primitive is no longer a proxy property access; use toRef/toRefs or a getter when a live connection is required.

State assignment happens synchronously, but DOM updates are batched. nextTick waits for Vue’s pending DOM update flush. It does not wait for a network request, image decoding, or every future render. Measure an element after the relevant update, not by guessing a timeout.

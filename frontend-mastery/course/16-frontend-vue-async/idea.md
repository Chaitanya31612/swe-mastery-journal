## Understand the idea

Use watch when you want a side effect tied to a specific source. watchEffect tracks reactive reads made during its synchronous execution; reads after the first await do not automatically become dependencies of that effect.

Register cancellation before awaiting. Vue 3.5 onWatcherCleanup must be called synchronously. The watch callback’s onCleanup argument is a useful alternative. Cleanup means the old request no longer owns this view, even if the network cannot be cancelled immediately.

Keep state transitions explicit. A stale response must not publish rows, an error, or loading=false. Decide whether an empty query clears results. Debouncing reduces request frequency but does not establish response order.

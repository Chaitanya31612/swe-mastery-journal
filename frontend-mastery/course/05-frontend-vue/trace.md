# Follow the execution

state.count is read through the proxy inside computed, so the dependency is tracked. Destructuring a primitive copies the current value into a plain variable. toRefs creates a linked access wrapper instead.

For a watcher, trace input change → old cleanup → new request → latest accepted result. onWatcherCleanup is a newer Vue 3 API; the callback cleanup parameter is another version-dependent choice.

Do not paste it into Vue 2.
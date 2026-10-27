# The idea

Vue tracks reactive reads and updates dependents when those values change. In Vue 3, reactive uses proxies for objects and ref holds a value accessed as .value in JavaScript.

A computed value derives a result and caches it until tracked dependencies change.

A watcher runs a side effect when its watched input changes. Use it for external work such as requests, not just to copy one derived value into another stored field.

Clean up obsolete work so old responses do not overwrite current state.

The work app uses Vue 2.6. It uses property getters/setters and has limits when adding properties or assigning array indexes.

Vue.set or array methods are relevant there. Vue 3 proxy behavior and newer watcher cleanup APIs must not be presented as Vue 2 behavior.
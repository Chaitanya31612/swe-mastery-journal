## Understand the idea

A route is part of the user’s working context. Search, selected workspace, and page often need to survive refresh or be shared.

Put those values in a stable URL contract and parse them, including invalid inputs.

A store is useful for shared application state and named actions. It does not automatically solve server cache freshness.

Keep remote data, local drafts, and permissions separate. With Pinia, storeToRefs preserves reactivity when destructuring state/getters; actions can be called from the store normally.

Route components can be reused when params change. Watching only onMounted can leave the old ticket on screen after navigation.

Watch the relevant ID or use a deliberate route data-loading strategy. A navigation guard improves UX but the server must still enforce access.
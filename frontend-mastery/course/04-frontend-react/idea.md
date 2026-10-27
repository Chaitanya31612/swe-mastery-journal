# The idea

A React render calculates UI from a snapshot of props and state. Event handlers created during that render see that snapshot.

Calling a state setter requests an update; it does not rewrite the local variable in the handler that is already running.

When the next value depends on the previous queued value, use a functional updater. Keep render pure: do not send requests or mutate outside objects while calculating JSX.

Effects synchronize with an external system after a committed render and need cleanup when applicable.

Keys identify sibling items across renders. Stable IDs preserve the right item identity.

Array indexes can attach local row state to the wrong item when the list is reordered. Memoization is a measured performance tool, not a correctness patch.
# The idea

A useful screen explains what is happening and what the user can do next. Design initial, loading, empty, ready, saving, failed, and retry states.

Keep an unsaved draft when a save fails. An empty list and a failed request should not look identical.

Use real buttons for actions and links for navigation. Labels must identify form controls.

Keyboard users need a visible focus indicator and a sensible focus order. Errors should name the field and explain a repair.

Color alone is not enough.

Performance starts with measurement. LCP concerns major content appearing, INP concerns responsiveness, and CLS concerns unexpected layout movement.

A fast API does not guarantee a responsive page if JavaScript blocks the main thread. Measure on representative devices and data.
## Understand the idea

The cascade considers origin/importance and layers before specificity and source order. A more specific selector is not always the winner across different layers or important rules.

Inspect the computed-style panel to see the actual winning declaration.

Use small component selectors and explicit state attributes/classes. Design tokens give repeated choices a name: spacing, surface, border, text, focus, and danger.

A token system helps consistency; it does not justify low contrast or shrinking a label to fit.

A component has states beyond the happy screenshot: hover, focus-visible, disabled, busy, invalid, empty, and high contrast preferences. Focus must remain visible against each surface.

A disabled appearance is not a substitute for explaining why an action is unavailable.
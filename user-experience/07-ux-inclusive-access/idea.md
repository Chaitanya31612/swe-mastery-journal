## Understand the idea

Accessibility is not a final color check. A person must be able to perceive the state, operate controls, understand the result, and use compatible assistive technology. Native HTML gives many behaviors that a clickable div does not.

Every interactive control needs an understandable name. Focus must be visible and move predictably. A modal needs a labelled dialog context, a deliberate focus path, and a way to close it. Errors and async status should be announced appropriately without narrating every keystroke.

Use WCAG 2.2 success criteria as requirements to check, with their exact scope and exceptions. Automated tools catch some issues; they cannot tell whether the action name makes sense or whether a real task is understandable. Combine automated checks, keyboard use, zoom, and assistive-technology testing.

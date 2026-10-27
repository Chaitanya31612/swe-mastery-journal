## Understand the idea

Build one vertical feature rather than a gallery of disconnected examples. A support workspace should open directly from a URL, load an allowed ticket list, filter it, open a ticket, edit its title, and preserve edits after a failed save.

Use a small boundary map: router owns context, an API adapter validates responses, a composable owns request lifetime, components render accessible states, and the server owns permission and concurrency rules. Add a store only for state that really crosses component ownership boundaries.

Completion is a demonstration: a happy path, a denied request, a failed save, a reverse-order request race, a keyboard path, and a large-data profile. Explain which evidence came from pure tests, component tests, and a browser.

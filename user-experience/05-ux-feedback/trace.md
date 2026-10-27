## Trace the execution

Trace click → acknowledged request → accepted job → processing → result or failure. Map each message to a real backend state.

An optimistic UI should explain pending state when the result is not yet confirmed.

For partial success, show successful and failed items separately with a retry policy. Do not make users reconstruct a 50-item selection from memory.
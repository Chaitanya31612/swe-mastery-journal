# Follow the execution

Begin with the user action. Editing a draft changes local unsaved state. Saving asks the server to change persisted state. A successful response updates the cached server record. A derived list recalculates from that cache and the URL filter.

For optimistic UI, record how to undo or reconcile a failed action. If two saves overlap, an old response must not erase a newer edit. A disabled button alone may not cover every caller.

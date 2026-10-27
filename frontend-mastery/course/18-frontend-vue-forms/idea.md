## Understand the idea

A form is a small state machine: pristine, editing, validating, saving, saved, or failed. Some checks are immediate, such as a required title. Others depend on the server. Avoid showing aggressive errors before a user has had a reasonable chance to enter a value.

Keep the draft when a request fails. A successful response may contain normalized data or a new version; accept that deliberately. If the record changed elsewhere, do not silently overwrite it. Use a version/ETag contract where the server supports it.

An error must say what can be fixed. Connect it to the field, keep the label visible, and focus a useful location after a failed submission. Disabling a button is not an explanation of why saving is blocked.

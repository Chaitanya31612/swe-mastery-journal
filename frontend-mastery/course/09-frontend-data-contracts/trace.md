## Trace the execution

Trace load → validate → adapt → edit draft → submit → accept server result. Keep server data separate from unsaved edits.

Test an absent field, explicit null, false, zero, and an empty string. They are five distinct cases.

If a nested structure is complex, copy the fields the form actually edits rather than cloning an entire model graph. structuredClone supports many values but not functions or every host object; it is not a universal serialization protocol.
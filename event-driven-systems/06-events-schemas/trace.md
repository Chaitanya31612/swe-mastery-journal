## Trace the execution

Business fact → envelope builder → serialization → broker bytes → consumer parsing → schema/business validation → effect. A valid JSON document can still be an invalid event.

For a new optional field, test an old consumer ignoring it and a new consumer handling its absence.

For a new event meaning, choose a deliberate version/type transition rather than silently repurposing a field.
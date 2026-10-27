## Break it and reason about the repair

A component that both owns a private value and blindly watches the parent prop can overwrite an in-progress edit. A custom input without a real label is harder to use even when v-model works.

**Remember:** Props describe. Events request. Slots compose.

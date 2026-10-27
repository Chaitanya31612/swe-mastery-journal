## Trace the execution

Parent changes modelValue → child renders it. User types → child emits a value → parent accepts it → new prop flows down.

This loop makes ownership visible.

For a wrapper, inspect whether id, aria-describedby, and class reach the actual input or only the wrapper div. Accessible names and error associations are part of the component’s contract.
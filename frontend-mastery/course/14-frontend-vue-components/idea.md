## Understand the idea

A component API is a small agreement. Props bring information in. Events ask the owner to change something. Slots let a caller supply presentation while the component owns behavior. Decide which part owns the saved value, draft, and focus.

Avoid mutating a nested object received as a prop. A shallow readonly prop boundary does not make every nested value immutable. Emit an update or edit an independent draft instead.

v-model is a prop/event convention. In Vue 3.4+, defineModel is a convenience macro. The older explicit modelValue plus update:modelValue contract is still useful to understand. Give events meaningful types and keep accidental HTML attributes from landing on the wrong element in wrapper components.

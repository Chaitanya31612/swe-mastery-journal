## Follow a concrete example

```vue
<script setup lang="ts">
defineProps<{ modelValue: string; disabled?: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
<template>
  <label>Ticket title
    <input :value="modelValue" :disabled="disabled"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)">
  </label>
</template>
```
The parent can use v-model="draft.title". Add an error slot only when callers need to customize that content; do not expose every internal DOM node as an API.
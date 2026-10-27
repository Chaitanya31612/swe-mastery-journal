## Follow a concrete example

```vue
<template>
  <p>{{ ticket.title }}</p> <!-- outside text stays text -->
  <!-- v-html="ticket.title" would interpret markup instead. -->
</template>
```

Use textContent for plain DOM text. For external links opened in a new tab, choose safe URL schemes and use rel="noopener noreferrer" where appropriate. A sanitizer for HTML does not automatically validate every business URL policy.

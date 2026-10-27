# Frontend · JavaScript & Vue 3

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [From URL to pixels](01-frontend-browser/README.md): Trace navigation, browser work, and the boundary between server and client.
- 02. [JavaScript values at API boundaries](09-frontend-data-contracts/README.md): Distinguish missing, null, false, zero, and shared nested state when adapting API data.
- 03. [JavaScript functions, closures, and object lookup](23-frontend-functions-objects/README.md): Predict captured values, call-time this, and property lookup in everyday UI code.
- 04. [Closures, tasks, and async races](02-frontend-runtime/README.md): Predict JavaScript ordering and prevent old requests from replacing new results.
- 05. [TypeScript: make invalid states harder to express](11-frontend-typescript/README.md): Model request states and narrow outside data instead of hiding uncertainty with any.
- 06. [CSS layout: size, flow, Flexbox, and Grid](24-frontend-css-layout/README.md): Choose a layout from content behavior and debug overflow instead of adding random widths.
- 07. [One owner for each piece of state](03-frontend-state/README.md): Separate source state, derived values, URL state, server data, and temporary UI state.
- 08. [Vue components: props, events, slots, and v-model](14-frontend-vue-components/README.md): Design a reusable component API with one owner and explicit update events.
- 09. [Vue tracks reads; versions matter](05-frontend-vue/README.md): Explain refs, computed values, watchers, and Vue 2 versus Vue 3 change detection.
- 10. [Make loading, errors, and controls understandable](07-frontend-experience/README.md): Design accessible states and measure a real user-visible delay.

## Intermediate

- 11. [Promises: overlap, cancel, and limit work](10-frontend-async-coordination/README.md): Choose sequential or parallel work and prevent stale results without losing useful failures.
- 12. [HTTP, browser caching, and the real network path](12-frontend-web-platform/README.md): Separate HTTP caching, application state, CORS, cookies, and request success.
- 13. [CSS cascade, tokens, and component states](25-frontend-css-systems/README.md): Explain why a style wins and build consistent states without escalating selector strength.
- 14. [DOM events, cleanup, and resource ownership](26-frontend-dom-lifecycle/README.md): Trace event propagation and release listeners, timers, observers, and subscriptions with their owner.
- 15. [Vue 3: refs, proxies, computed, and timing](13-frontend-vue-reactivity/README.md): Follow a tracked read and explain why nextTick differs from ordinary assignment.
- 16. [Composables: reusable behavior without hidden global state](15-frontend-vue-composables/README.md): Extract reactive behavior with explicit inputs, lifecycle cleanup, and a predictable return API.
- 17. [Vue watchers and async search without stale state](16-frontend-vue-async/README.md): Implement a watched request with cleanup, current-result guards, and honest loading/error states.
- 18. [Vue Router and Pinia: choose where state lives](17-frontend-vue-routing-store/README.md): Use URL state, component state, and stores deliberately, including route changes and server rendering.
- 19. [Forms that survive real editing](18-frontend-vue-forms/README.md): Handle validation, dirty state, unsaved changes, and server conflicts without losing user work.
- 20. [Browser rendering and performance evidence](27-frontend-rendering-budget/README.md): Separate network, JavaScript, layout, paint, and rendering costs before optimizing a screen.
- 21. [Vue performance: measure the expensive boundary](19-frontend-vue-performance/README.md): Find whether a slow interaction comes from work, rendering, layout, or network delay.
- 22. [Vue tests: behavior, timing, and contracts](20-frontend-vue-testing/README.md): Write component tests for failed saves, async races, and accessible interaction.
- 23. [Frontend security that affects everyday code](21-frontend-browser-security/README.md): Separate trusted markup, outside text, browser storage, and server authorization.
- 24. [React renders snapshots](04-frontend-react/README.md): Explain stale closures, functional updates, effects, keys, and render purity.
- 25. [Next.js: server/client boundaries and freshness](06-frontend-next/README.md): Place code at a deliberate execution boundary and explain which cache is being refreshed.
- 26. [Debug and test a complete frontend flow](08-frontend-capstone/README.md): Prove one task-editing flow across state, requests, rendering, and accessibility.
- 27. [Ship a Vue 3 support workspace](22-frontend-delivery-capstone/README.md): Connect URL state, reusable components, async data, editing, tests, and measured UX in one small feature.

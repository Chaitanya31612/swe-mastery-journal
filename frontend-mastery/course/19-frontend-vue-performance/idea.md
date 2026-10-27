## Understand the idea

Start with a measured symptom: typing takes 200 ms to appear with 5,000 tickets. Profile before choosing a fix. Filtering, component updates, layout, and network work have different repairs.

Stable props can reduce avoidable child updates. Stable keys preserve identity. Code splitting reduces initial work for features the user has not opened. List virtualization reduces mounted rows, but it must preserve focus, keyboard navigation, and scroll expectations.

Do not memoize a correctness bug. A wrong state owner or stale response remains wrong when cached. shallowRef, v-memo, and custom optimizations add contracts that future maintainers must understand. Use them after identifying a meaningful cost.

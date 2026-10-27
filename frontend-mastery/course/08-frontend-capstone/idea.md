# The idea

Debug from an observed symptom. Write the exact steps, expected result, and actual result.

Decide which boundary could explain the difference: URL, state ownership, request ordering, server response, cache, rendering identity, or browser layout.

Unit tests suit pure transformations. Component tests suit interaction and visible states.

A small end-to-end test checks that important boundaries connect. Avoid replacing every dependency with a mock and calling the result a full application test.

Capstone: a searchable task list with a URL filter, editable title, save failure recovery, stable row identity, and stale-response protection.

Use either React or Vue for the implementation, then explain the same state ownership in the other framework. Next.js is an optional boundary exercise, not a reason to rebuild every screen.
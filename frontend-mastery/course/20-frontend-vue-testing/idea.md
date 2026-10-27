## Understand the idea

A pure test checks a transformation. A component test mounts a small UI and exercises its public behavior. A browser test verifies real navigation, layout, and browser APIs. Choose the layer that can observe the defect.

Prefer accessible roles and labels when finding controls. A test that clicks .blue-button can pass while the button has no useful name. Wait for Vue updates and promises deliberately. nextTick flushes Vue updates; flushPromises helps pending promise callbacks in tests. Neither proves a real remote service works.

Control time and request outcomes. Resolve B before A to test a race. Return an HTTP rejection to test draft preservation. Keep a few real integration checks so mocks do not invent an API contract that the server does not provide.

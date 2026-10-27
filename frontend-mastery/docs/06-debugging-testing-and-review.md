# Debugging, testing, and review

Write the symptom before changing the code. Name the user action, expected result, actual result, and smallest dataset that reproduces it.

Trace one path: event → state owner → request → accepted response → render → visible feedback. Check URL, server freshness, row keys, and cleanup when relevant.

Use a pure unit test for a transformation. Use a component test for interaction and loading/error states. Use a small browser test for direct navigation, keyboard behavior, and real layout. One layer does not replace the others.

For async races, control promises or responses. Resolve request B before A and assert that B stays visible. Guard loading and errors too. Fixed sleeps do not prove the intended state happened.

Review questions:

- Is each fact stored in one place?
- Can old work overwrite newer work?
- What survives a failed save?
- Can a keyboard user complete the task?
- Does a fresh direct URL work?
- Which cache can return old data?
- What test would fail before this repair?

The [interactive capstone](../course/08-frontend-capstone/README.md) connects these questions to a task-editing flow. Existing staff exercises remain optional deeper practice.

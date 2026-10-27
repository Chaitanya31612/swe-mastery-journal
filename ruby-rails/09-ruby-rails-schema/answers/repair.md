# One valid repair

Add a matching database unique constraint/index, normalize values consistently, and handle conflicts at the use-case boundary. Resolve existing duplicates before adding it. Imports may bypass validations; test that direct database writes still cannot violate the rule.

**How to check:** Concurrent requests can both pass application checks. The database must reject conflicting stored keys.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

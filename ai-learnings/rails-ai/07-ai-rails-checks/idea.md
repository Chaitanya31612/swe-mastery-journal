## Understand

Business tests use controlled provider outputs to prove the application accepts and rejects the right states. Adapter tests check request mapping, completion/refusal handling and transport failures. Live evaluations measure how a chosen model behaves on representative tasks. A passing test in one layer does not replace the other two.

Use adversarial fixtures: extra filter fields, cross-tenant IDs, unknown evidence IDs, correct numbers with wrong categories, ambiguous names, oversized context, stale results, permission revocation, provider timeout and an agent step limit. Keep private records out of fixtures; synthetic counterexamples are often clearer.

Test no-model behavior as a first-class path. The ordinary filter/table and reviewed rule guidance should remain useful. Verify that generated text is escaped, source labels are honest and long/mobile content does not hide controls.

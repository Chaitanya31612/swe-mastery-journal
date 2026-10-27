## Trace the execution

Observed regression → minimal deterministic check → known-good/bad commits → bisect or exact-snapshot comparison → inspect trigger → preserve regression test. Keep the active worktree’s edits untouched.

A first-bad dependency update is a trigger to investigate, not automatically the root explanation. Reproduce the mechanism after locating the change.
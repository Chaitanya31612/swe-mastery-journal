## Trace the execution

Two components call useSelection. Each call allocates one ref, so they can select different tickets. Move the ref above the function and both callers now share it. Neither version is automatically better; the intended ownership decides.

Test composables with pure seams when possible. For lifecycle-dependent behavior, mount a small component and verify listeners are removed when it unmounts.

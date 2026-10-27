# One valid repair

Define the expected recoverable errors and handle only those. Raise or return a clear typed result for invalid user input.

Let unexpected errors reach monitoring. Use ensure/block cleanup without replacing exceptions.

Test each intended error separately.

**How to check:** Bundler uses the project’s dependency definitions and lockfile to resolve gems for that command.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
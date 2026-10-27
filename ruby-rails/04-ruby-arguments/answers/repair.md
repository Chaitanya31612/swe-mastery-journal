# One valid repair

Use def call(*args, **kwargs, &block); target(*args, **kwargs, &block); end. Test positional inputs, required and optional keywords, false values, and a passed block.

Verify both the work Ruby and the planned upgraded Ruby in isolated environments.

**How to check:** Closures can observe later assignments to captured variables. Freezing and copying are separate choices.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
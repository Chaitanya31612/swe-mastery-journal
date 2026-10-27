# One valid repair

Load through an allowed scope such as current_user.tasks.find(id), and enforce the action policy if ownership is not the whole rule. Test user A cannot change user B’s task even by sending HTTP directly. Confirm title and owner remain unchanged.

**How to check:** Strong parameters filter assignable attributes. Ownership and authentication are separate checks.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.

# The idea

A closure carries access to variables from its surrounding scope. It does not take a frozen snapshot of every value.

If that variable changes, the closure can see the new value. This is useful for callbacks and risky for long-lived captured state.

A lambda behaves like a small method: it checks argument count more strictly and return leaves the lambda.

A non-lambda proc can return from the method where it was defined; after that method has ended, such a return can raise LocalJumpError. Use lambdas when you want method-like callback behavior.

Ruby 2.7 is a transition version for keyword arguments. Code that forwards a final hash as keywords may warn there and fail on Ruby 3.

Be explicit about positional arguments, keyword arguments, and a block.
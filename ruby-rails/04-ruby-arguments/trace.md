# Follow the execution

Split the call into three envelopes: positional values in args, named values in kwargs, behavior in block. Forward each explicitly.

In Ruby 2.7, warnings are useful migration signals; do not silence them without understanding the call shape.

For the closure, reader keeps access to the label binding. Reassignment changes what that binding points to.

For a snapshot of text, create a separate value deliberately, such as label.dup.freeze when a shallow frozen string is what you need.
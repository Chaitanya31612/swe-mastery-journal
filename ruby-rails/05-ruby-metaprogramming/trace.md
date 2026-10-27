# Follow the execution

The class body runs as Ruby code. It iterates over LABELS and adds two instance methods. Calling done_label then uses normal method lookup. No generated source string is needed.

For a Rails concern or DSL, ask four questions: when does this declaration run, which object is self, which methods get defined, and which hooks are registered? Trace one declaration all the way to a runtime call.

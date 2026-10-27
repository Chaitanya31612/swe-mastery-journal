## Understand the idea

Callbacks can protect local lifecycle rules, but they can also hide a large workflow behind save. A concern may register callbacks when included.

Search declarations and callers before assuming the method body is the whole behavior.

First map what actually happens: validation, transaction, callback, database write, after_commit, enqueue, and external effect.

Rails 4.2 callback halting and exception behavior differ from newer versions; verify the exact fork/version rather than pasting modern throw(:abort) guidance into legacy code.

Move orchestration in small steps. Keep an observed behavior test, introduce an explicit use case, route callers through it, and remove duplicate callback paths only when their coverage is clear.

Do not fire the event both explicitly and through the old callback.
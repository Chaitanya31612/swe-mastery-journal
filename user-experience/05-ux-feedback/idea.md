## Understand the idea

After an action, people need to know whether the system heard them, whether work is still running, and what changed.

“Saved” means something different from “Queued.” A progress indicator must describe the boundary it actually observes.

Use a determinate bar only when you know a meaningful total. Use a clear waiting state otherwise.

Approximate response-time heuristics can help thinking, but no single threshold fits every network and task. Tell people what they can safely do while waiting.

Prevent predictable errors where possible. For reversible actions, an understandable Undo can be less disruptive than repeated confirmation dialogs.

For irreversible or high-consequence actions, make the target and consequence explicit. A confirm dialog that says only “Are you sure?” adds interruption without understanding.
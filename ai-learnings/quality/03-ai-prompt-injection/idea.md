## Understand

Prompt injection places hostile or irrelevant instructions in user text, retrieved documents, tool results, or other context. The goal may be to override the task, reveal data, trigger a tool, or change the answer. A document can contain both useful facts and an instruction the application must not obey.

Use layered controls: minimize capabilities, scope data before exposure, separate trusted instructions from outside content, validate tool proposals and output, restrict egress, and require precise approval for consequential actions. A detector or sanitizing prompt can help some cases but is not a complete boundary.

Treat model output as outside input too. Do not execute generated HTML, SQL, shell commands or URLs without a separate deliberate contract. A retrieved page cannot grant the user new privileges. Test indirect instructions across multiple turns and tool results, not only “ignore previous instructions” typed directly by the user.

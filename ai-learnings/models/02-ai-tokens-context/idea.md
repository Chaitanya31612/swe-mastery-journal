## Understand

A token is a model-specific unit of text or other encoded input. It may be a word fragment, punctuation, or bytes. Token count is not character count. Different languages, code, and tokenizers produce different counts.

The context window bounds what a request can process under the selected model’s rules. Instructions, user messages, conversation history, tool definitions, retrieved passages, and tool results all compete for space. Output and, on some models, internal reasoning also have limits or budget implications. Check the selected API rather than assuming one universal formula.

A model call does not automatically remember every previous request. The application or a provider conversation service supplies the context. Keep essential policy and current evidence. Trim stale content deliberately; do not split a tool request from its result. A long window is capacity, not proof that the model will use every detail correctly.

## Understand

For a typical decoder-based text LLM, input is tokenized and converted to numeric representations. Transformer layers combine information across permitted positions using attention and other learned transformations.

The result supports a distribution over possible next tokens. The system selects or samples a token, then continues.

Attention is a learned weighting mechanism, not a database query or a reliable explanation of why a claim is true. The original Transformer paper describes a broader architecture; modern production models vary.

You do not need to implement a Transformer to design its application boundary.

Serving often separates **prefill**, processing the input context, from **decode**, generating further tokens. A key/value cache can reuse intermediate attention state during generation.

That cache is neither a business database nor a guarantee that a future independent request will remember the conversation.
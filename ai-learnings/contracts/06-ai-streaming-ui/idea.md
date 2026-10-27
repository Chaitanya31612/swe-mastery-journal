## Understand

Streaming sends incremental events so the UI can show progress before completion. It changes delivery timing, not the correctness of the answer. Provider streams can include text, tool-call arguments, usage, refusals, errors, and completion signals; do not assume every event is display text.

Keep a state machine: queued, running, partial, validating, completed, unavailable, cancelled, or expired. Do not mark the operation successful because the first bytes arrived. Do not execute a tool from partial JSON arguments. Buffer a complete validated proposal before applying it.

For a Rails browser flow, a background job can write run events and the client can read status through polling or a controlled streaming channel. Bound buffers, escape generated text, preserve keyboard focus, and cancel obsolete views. A disconnected browser must not cause a partial answer to be stored as a completed one.

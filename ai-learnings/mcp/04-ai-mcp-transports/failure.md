## Break it and remember

Logs on stdout can break stdio parsing. A globally cached actor can leak one user's identity into another request.

A proxy can buffer a stream and erase expected progress behavior.

**Memory cue:** Choose a transport; then trace the entire deployment path.
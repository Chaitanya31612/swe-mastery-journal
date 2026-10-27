## Understand

A tool exposes a callable operation with a schema. A resource exposes identifiable context that a host can read through the protocol. A prompt exposes a reusable message/workflow template. They serve different interaction patterns; none automatically authorizes a user to see its underlying data.

A host may also support capabilities such as sampling or elicitation under a selected revision/SDK. These are negotiated features, not assumptions every peer supports. Sampling can introduce server-initiated model work; elicitation can request user input. Keep cost, consent, and data boundaries explicit.

Tool annotations can hint that an operation is read-only or idempotent. They are advisory metadata. The implementation and host/server policy must enforce actual behavior. Likewise, resource URIs and filesystem roots are not substitutes for an application access check or OS sandbox.

# Chat: durable acceptance, live delivery, and reconnects

Learning outcome: Separate transport from durability, implement retry-safe messages and catch-up cursors, and state presence/order limits.

## Define message states before sockets

“Sent” can mean accepted by our store, transmitted to a gateway, acknowledged by one recipient device, or read by a user. Clarify one-to-one versus groups, history retention, offline delivery, ordering, presence, and multi-device synchronization. A WebSocket supplies persistent bidirectional transport; it does not persist a message or guarantee a disconnected recipient received it.

## Canonical messages and soft routing

Use conversation identity and membership, message identity, sender/client request identity, sequence/order metadata, and body/reference. Scope retry identities so repeated sends return the same logical message but distinct intentional messages do not merge. Assign per-conversation order at a serialized/fenced ownership or another suitable append protocol; arbitrary timestamps from independent senders are not an ordering proof.

Connection gateways own sockets and buffers. A connection registry maps devices to current gateways, but is rebuildable/soft state. Durable history is authoritative. Gateways can scale by live-connection/memory/network limits; message-service capacity may scale differently. Drain sockets during deployments and control reconnect storms.

## Trace sender, receiver, and offline recovery

Sender authenticates and proves conversation membership → service validates/deduplicates request → durable append → accepted response → delivery work. Recipient device acknowledges according to the defined receipt meaning. A disconnected device later requests messages after its durable cursor. The client applies messages idempotently and advances the cursor only under safe ordered processing semantics.

A crash after append before response makes the sender uncertain; replay with the same client request identity returns the existing message. A delivery worker crash or disconnected gateway can repeat notifications; history/cursors allow recovery without assuming every push is reliable. Push notification itself can be best-effort signaling when history remains authoritative.

## Presence and group fan-out

Heartbeats and TTL expiry approximate online status. Power/network loss is not instantly knowable. Presence on one device may differ from user-wide presence. For groups, membership, fan-out amplification, and per-conversation ordering affect capacity. Large broadcast groups may need different distribution from small interactive rooms.

## Operate and evolve

Measure acceptance latency, online delivery delay, catch-up lag, active connections, buffered bytes, dropped connections, and reconnect rate. Enforce rate limits and membership on sends/reads; protect stored content and retention. End-to-end encryption is a distinct architecture requirement that changes searchable content, key management, and device flows. Roll out message schema/protocol versions with old client compatibility and bounded buffering.

## Retrieve before practicing

Explain accepted versus delivered versus read. Trace a retry after commit and a reconnect after a missed live message.

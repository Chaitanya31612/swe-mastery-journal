# Chat: durable acceptance, live delivery, and reconnects — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Multi-device chat

500,000 connected devices, ten million messages/day, 10× message peak, 4 KB average stored message. Keep history 90 days. Users can have three devices. Require durable acceptance, per-conversation order, and offline catch-up; presence may be approximate. Estimate message and connection limits and design retry/reconnect/membership flows.

## P2 — Add a large room

Add a room with 100,000 connected recipients receiving ten messages/s. Explain network/fan-out pressure, backpressure for slow consumers, history catch-up, and where you would partition or specialize distribution.

## P3 — Fix bad pseudocode

```text
message_id = wall_clock_ms()
socket.send(message)
return "durably sent"
```

There is no durable append or client request identity. Repair acceptance and retry semantics; explain how ordering is assigned.

## Delayed gate

Explain accepted versus delivered versus read. Trace a retry after commit and a reconnect after a missed live message.

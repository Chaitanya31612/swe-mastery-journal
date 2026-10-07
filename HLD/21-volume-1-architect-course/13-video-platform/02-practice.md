# Video delivery: control plane, data plane, and processing — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Training-video portal

20,000 uploaded videos/day, 100 MB average source, 30-day source retention, renditions total three times source bytes, and 50,000 concurrent viewers at 3 Mb/s average. Tenant-private access, resumable uploads, and processing status are required. Design transfer authorization, processing DAG, ready publication, CDN access, and deletion/failure behavior.

## P2 — Change to live streaming

Now a small subset needs live streams with a two-second glass-to-glass target. Identify which on-demand assumptions break and what latency/packaging/distribution choices require new design. Do not pretend the original batch job graph automatically meets it.

## P3 — Repair the proposal

“Upload all video bytes through one API instance, mark ready when the upload starts, and cache private manifests publicly for a day. Retry transcoding by overwriting the currently served object.” Explain which contract each action threatens.

## Delayed gate

Trace upload-to-ready and identify the durable intent and publication boundary. Recompute egress when bitrate doubles.

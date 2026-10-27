## Trace the execution

Manifest desired state → API admission → controller reconciliation → scheduler/capacity → pod process → readiness → service traffic. Then trace a pod reschedule and a rollout with the DB unchanged.

Map every secret, network permission, and persistent data store to its owner. A healthy control plane does not prove your app is healthy.

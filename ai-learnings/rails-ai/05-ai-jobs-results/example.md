## Walk through an example

```text
POST request → queued run → job claim → current facts → model → validator → completed result
GET run → current actor and source-version checks → result, pending, stale, or unavailable
```
The lab documents its queue durability limits. It is not a claim that a local thread queue provides production delivery guarantees.
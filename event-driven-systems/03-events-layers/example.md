## Follow a concrete example

```text
Rails → Ruby client → metadata discovery → partition leader
                           producer batch → replicated append
Reporting client ← fetch records ← partition log
KRaft controller quorum → cluster metadata/leadership
```
Distinguish data-plane record traffic from control-plane metadata decisions. A controller outage and a consumer bug are different failure classes.
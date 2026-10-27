## Follow a concrete example

```text
Rails read cache → rebuildable ticket summaries, bounded TTL
Background-job Redis → deliberate job durability/memory policy
Session store → explicit loss and logout behavior
```
Different roles may need separate instances or clusters. A shared endpoint is not free simply because the client library looks the same.
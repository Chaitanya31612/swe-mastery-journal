## Follow a concrete example

```text
reporting-v1 → current projection and inbox
reporting-v2-rebuild → separate group + separate projection/inbox identity
Compare counts/state on a known synthetic dataset.
Switch reads deliberately after verification.
Do not invoke notification sending from the rebuild projector.
```
A schema change may require upcasting/translation of old events. Document the old contract rather than silently reading old bytes with new assumptions.
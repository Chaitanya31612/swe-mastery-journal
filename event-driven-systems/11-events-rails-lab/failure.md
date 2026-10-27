## Break it and reason about the repair

The lab is intentionally one broker and one serial dispatcher. It does not prove multi-zone HA, high-throughput ordering under several dispatchers, production auth, or every legacy-fork behavior.

**Remember:** One file, one boundary, one observable state.
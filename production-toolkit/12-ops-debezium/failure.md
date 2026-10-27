## Break it and reason about the repair

CDC may expose columns not intended for downstream systems if schema/filtering is careless. A stopped replication slot/log reader can grow retained WAL. Running both polling and CDC publishers without coordination can duplicate events.

**Remember:** Committed change is the source. Business meaning is your contract.

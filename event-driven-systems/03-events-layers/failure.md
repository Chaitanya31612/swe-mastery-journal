## Break it and reason about the repair

One local broker hides replica/failover behavior. Acknowledgement settings cannot create replicas that do not exist.

Confusing controller roles with business consumers makes diagnosis random.

**Remember:** Client → leader log → replicas; controller manages metadata.
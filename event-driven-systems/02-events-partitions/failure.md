## Break it and reason about the repair

A key is not a global lock. A large number of partitions is not free operationally.

Changing keys can scatter one entity’s history.

**Remember:** Order lives inside a partition, not in the topic name.
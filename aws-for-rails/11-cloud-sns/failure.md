## Break it and reason about the repair

Putting all independent subscribers on one queue makes them compete for messages instead of each receiving all required facts. An overly broad queue policy can allow unintended senders.

**Remember:** One queue shares work. Fan-out copies responsibility.
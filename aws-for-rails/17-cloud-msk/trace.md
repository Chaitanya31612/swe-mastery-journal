## Trace the execution

Client contacts bootstrap → discovers leaders → authenticates/connects to actual brokers → produces keyed record → group consumes/commits under its own policy. Debug network, auth, topic access, and business processing separately.

Retention and consumer downtime interact. A lagging consumer can lose required history after retention; managed brokers do not extend the business recovery window automatically.
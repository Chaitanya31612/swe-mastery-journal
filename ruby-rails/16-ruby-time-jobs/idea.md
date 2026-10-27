## Understand the idea

“Tomorrow at 9” needs a time zone and a calendar rule. Store an instant for an event that already happened.

Store the intended zone/rule as well when scheduling future local-time behavior. Daylight-saving transitions can create missing or repeated local times.

cron or a scheduler triggers work. It does not guarantee exactly one business run.

Two schedulers, retries, or a delayed process can trigger the same logical period more than once. Define a unique run key such as workspace plus report date, backed by a database rule.

A job should load current state, tolerate retry according to its contract, and expose a useful outcome. Passing an ID is usually better than serializing a whole model object.

A scheduled trigger and a durable work record are different things.
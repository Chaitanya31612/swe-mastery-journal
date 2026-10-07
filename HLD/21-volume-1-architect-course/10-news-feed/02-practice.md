# News feed: projections, fan-out, and privacy — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Chronological feed

Two million active users/day, average 100 followed authors, 400,000 posts/day, ten feed reads/user/day. One author has ten million followers; ordinary authors have at most 500. Feed freshness may lag 30 seconds; private-post access revocation must take effect within two seconds. Design push/pull choice, source/projection data, pagination, retries, and access checks.

## P2 — Team activity dashboard

Adapt the projection approach to tenant-isolated project activity with only 50 members/project. New events appear within five seconds; deleted sensitive events must disappear promptly. Which fan-out and permission assumptions change?

## P3 — Repair the proposal

“Copy full private post bodies into follower caches for a day. Every celebrity write updates all followers synchronously. Offset page 2 always means the next 20 posts.” Identify performance, freshness/privacy, and paging problems.

## Delayed gate

Compare push, pull, and hybrid with a celebrity. Explain why eventual feed freshness does not imply eventual permission enforcement.

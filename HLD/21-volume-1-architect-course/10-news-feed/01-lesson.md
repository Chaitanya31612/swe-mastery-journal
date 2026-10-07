# News feed: projections, fan-out, and privacy

Learning outcome: Choose push/pull/hybrid from follower skew and freshness, design stable pagination, and preserve access on derived views.

## Separate canonical posts from derived feeds

A post is authoritative content with owner, visibility, identity, and version/deletion state. A home feed is a derived ordered selection of posts a viewer may see. Ask chronological versus ranked ordering, freshness, follow relationships, media, pagination, deletion, and privacy. A chronological feed needs less machinery than a personalized ranking platform.

Push/fan-out-on-write places references into followers’ feed projections when a post is created. It makes reads cheap but amplifies writes and creates lag/replay work. Pull/fan-out-on-read merges followed authors’ recent posts when a viewer reads, trading read complexity for less publication work. A hybrid can push ordinary authors and pull high-fan-out authors, but the threshold depends on distribution, active followers, write/read rates, and operational cost.

## Estimate amplified work

Publication work is roughly posts × recipients for push, not just the post creation QPS. A celebrity can dominate fan-out even if averages look fine. Active-viewer materialization and bounded retention can reduce work. Store post references rather than duplicating the entire body when access/version semantics favor it. Make projection updates idempotent, e.g. a unique viewer/post pair.

## Trace both flows

Publish authenticates author, commits post plus event intent, then workers update derived feeds. Read obtains ordered candidate references, resolves content, checks current access/deletion requirements, and returns a page. A lagged feed projection is not a safe authority for private-post access. Revocations may require authoritative filtering and/or a bounded propagation contract.

Cursor pagination uses a stable ordering key such as creation time plus unique ID for chronological feeds. Offset pagination can shift when new items arrive. A cursor needs a consistent snapshot/window policy if exact no-duplicate/no-missing paging is required; ranking changes complicate this further. State the promised behavior rather than declaring cursors solve every ranking issue.

## Failure and evolution

Rebuild projections from canonical posts/events where retention permits it. Measure fan-out lag, visible freshness, duplicate/missing feed entries, access violations, and read latency. A hot-author policy must preserve pagination and merge semantics. Roll out ranking/projection versions compatibly; shadow read comparisons can reveal differences before switching.

Authorization, deletion freshness, and high-fan-out load are more informative deep dives than naming a specific cache brand. Personalization is a separate expanded scope, not a reason to introduce every recommendation component by default.

## Retrieve before practicing

Compare push, pull, and hybrid with a celebrity. Explain why eventual feed freshness does not imply eventual permission enforcement.

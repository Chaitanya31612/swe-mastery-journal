# Crawler scheduling, bounded exploration, and safe fetching — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Documentation crawler

Crawl ten million allowed pages/day, 100 KB average retrieved body, with a peak factor of two. Mean fetch time is 0.5 seconds. Each host allows at most one fetch every two seconds. Store new content for 30 days. Design scheduling/ownership, deduplication, restart recovery, and the safety boundary. Explain aggregate capacity versus one-host capacity.

## P2 — Recurring refresh

Some pages change hourly; others yearly. Design adaptive refresh priority without starving slow sites. Decide which metadata and signals guide the schedule, and how failures affect retry/freshness.

## P3 — Fix bad pseudocode

```text
for url in discovered_links:
    if not visited.contains(url):
        visited.add(url)
        spawn_unlimited(fetch(url))
```

Identify concurrency, politeness, resource, recovery, and destination-safety failures. Write a bounded task lifecycle.

## Delayed gate

Explain why per-host scheduling, duplicate content detection, and URL identity are three different problems.

# Autocomplete: derived indexes, top-K, and fresh snapshots — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Popular prefix completion

Five million users/day, 20 searches/user, six autocomplete requests/search. Serve five suggestions within p95 100 ms at the API boundary. Popularity may lag one hour, but blocked queries must disappear within five seconds. Explain ingestion, scores, serving structure, version publication, hot prefixes, and removal overrides. Use a 5× peak.

## P2 — Private employee-name search

Transfer to 10,000 tenants, each with up to 20,000 employee names. A user may see only authorized tenant/directory entries. Explain keying, cache sharing, prefix indexing, freshness, and why the popular-query pipeline may be unnecessary.

## P3 — Fix bad response handling

```text
on_input(text):
    request_suggestions(text).then(results => show(results))
```

Trace out-of-order responses and repair the client contract. Separately review “overwrite trie nodes in place during rebuild.”

## Delayed gate

Compare batch freshness with emergency removal. Explain why client response order and server index publication are separate mechanisms.

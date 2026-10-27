## Understand

Several caches can exist in one AI request. Provider prompt caching may reuse eligible input-prefix computation under provider-specific rules.

An embedding cache avoids recomputing a representation. A retrieval cache stores candidates.

An answer cache stores a product result. None automatically shares the others' freshness or access guarantees.

Key answer reuse by the actual task and authority: normalized inputs, tenant/permission scope, source/evidence/rule versions, prompt/model contract versions, and relevant retrieval settings. Recheck current access before returning stored content.

Avoid a cache keyed only by human question text.

Define what invalidates or expires each cache. A TTL can bound some staleness but cannot justify serving a now-forbidden document.

Don't cache incomplete, refused or invalid output as a completed answer. A cache hit should remain visible in debugging metadata.
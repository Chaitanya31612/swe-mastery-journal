## Understand

A useful retrieval pipeline begins before embeddings. Load permitted sources, parse them, preserve headings/tables and provenance, clean carefully, attach access metadata, create chunks, and publish a versioned index.

Each step can lose information.

Keep source ID, source version, location/page/section, tenant/access class, parser version, chunking version, and embedding version. Make ingestion idempotent by source/version identity.

Publish a complete new index or source revision deliberately so queries do not see half an update.

Deletion and permission changes need a propagation path. A document removed from the file browser may still exist in an index or answer cache.

Recheck current authorization before returning evidence. Track ingestion lag and failures as product freshness signals, not only background-job errors.
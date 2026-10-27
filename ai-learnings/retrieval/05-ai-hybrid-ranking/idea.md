## Understand

Lexical search is useful for exact identifiers, rare terms, and matching words. Dense vector search can help with paraphrases. Hybrid search combines candidate signals. A reranker examines a query and candidate more directly to improve ordering. Each adds a different cost and failure mode.

Do not add raw scores from unrelated systems without a defined, evaluated normalization. Rank fusion, such as reciprocal-rank fusion, combines positions rather than assuming scores share units. Rerank only permitted candidates and keep collection sizes bounded.

Separate candidate recall from final ranking. If the correct document never enters the candidate pool, a reranker cannot recover it. If it appears but is discarded during context assembly, retrieval itself may be fine. Trace the stage where evidence disappears.

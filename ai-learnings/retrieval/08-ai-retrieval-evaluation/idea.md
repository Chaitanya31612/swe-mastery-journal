## Understand

Create realistic questions with expected supporting documents/spans and answerability labels. Include paraphrases, exact terms, exceptions, stale documents, forbidden documents, ambiguity, and no-answer cases. Freeze a held-out set before tuning.

Recall@k asks whether expected relevant evidence is among the first k results under a defined relevance label. Precision@k asks how much of the retrieved set is relevant. Ranking metrics measure order. These are not final-answer accuracy, and relevance labels may have multiple valid supporting sources.

Check the pipeline in order: parsed source quality, candidate recall, ranking/context packing, answer support, access boundaries, latency and cost. Use an exact/scoped or lexical baseline. Keep permission leakage as a separate hard failure, not a small penalty hidden by an average relevance score.

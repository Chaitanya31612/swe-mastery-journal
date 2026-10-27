## Understand

A rubric states what counts: supported claims, correct scope, useful uncertainty, allowed actions, and clear next steps. Exact checks should handle exact fields. Human review and model-based judges can help assess prose, but judges can disagree, prefer certain styles, or make the same mistakes as the system being judged.

Validate any judge against a reviewed labelled set. Hide irrelevant model identities where useful, vary order in pairwise comparisons, and inspect disagreements. A judge score is a measurement with limits, not an oracle. Keep severe boundary checks deterministic where possible.

Calibration asks whether stated probabilities match observed frequencies under a defined task and dataset. Thresholding an uncalibrated score does not make it calibrated. Precision asks how many accepted positives are correct; recall asks how many actual positives were accepted. Their tradeoff depends on the cost of mistakes and fallback capacity.

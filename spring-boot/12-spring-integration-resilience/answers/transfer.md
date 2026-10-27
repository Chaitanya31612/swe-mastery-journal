## One valid transfer

You can persist intent and track attempts, but a crash between remote acceptance and local acknowledgement leaves uncertainty. Use a provider status lookup/reconciliation if possible, tolerate duplicates where acceptable, or escalate ambiguous outcomes. Do not promise universal exactly-once sending.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.

## One valid repair

Store inbox/dedup and the local report effect in the same DB transaction, protected by a unique key. Commit Kafka only afterward. Test failure after inbox insert and before effect so both roll back.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.

# Unique IDs: clocks, coordination, and order — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. Rough timestamp sorting establishes what?
   - A. Global causal order
   - B. Only approximate physical-time order under assumptions
   - C. A distributed transaction
   - D. Unforgeable authorization

2. The sequence field exhausts within the same timestamp. What is safe?
   - A. Wrap silently
   - B. Remove the worker field
   - C. Wait/backpressure or select another valid scheme
   - D. Ignore duplicates

3. Clock synchronization proves no rollback?
   - A. Always
   - B. Only with more workers
   - C. Only with larger integers
   - D. No; rollback needs an explicit policy

4. Why use disjoint leased ID ranges?
   - A. Reduce per-ID coordination while preserving allocation ownership
   - B. Guarantee gapless numbering after failures
   - C. Remove durable allocation state
   - D. Provide encryption


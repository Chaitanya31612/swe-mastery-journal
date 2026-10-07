# Crawler scheduling, bounded exploration, and safe fetching — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. More workers can increase one host beyond its agreed rate?
   - A. Always
   - B. Only if the queue is long
   - C. Yes with a new hash
   - D. No; policy remains a constraint

2. What does a Bloom filter risk?
   - A. False positives rejecting unseen items
   - B. No memory usage
   - C. Perfect exact membership
   - D. Automatic content equivalence

3. Why validate redirect destinations too?
   - A. For prettier URLs
   - B. The effective destination can cross a forbidden boundary
   - C. To create more threads
   - D. To ensure two bodies are identical

4. Why distinguish discovered from completed?
   - A. There is no difference
   - B. It speeds DNS automatically
   - C. Crashes/retries must not strand discovered work
   - D. It removes retention policies


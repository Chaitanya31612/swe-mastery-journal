# URL shortener: serving and mutable mappings — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. Base62 chiefly provides what?
   - A. Authorization
   - B. A uniqueness protocol
   - C. Compact representation
   - D. Encryption

2. Two generators choose the same random code. What closes the normal insertion race?
   - A. Cache absence
   - B. A pre-insert SELECT alone
   - C. Longer URLs always eliminate collisions
   - D. Durable unique insert with collision retry

3. Prompt revocation primarily constrains what?
   - A. Freshness of every serving/cache layer
   - B. Only URL length
   - C. Only owner name
   - D. Only analytics counters

4. A cold cache at peak requires what analysis?
   - A. Normal hit rate proves safety
   - B. Source fallback load and bounded admission
   - C. Unlimited retries
   - D. A bigger client cache regardless of policy


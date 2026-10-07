# Distributed rate limiting and overload control — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. A token bucket with rate r and capacity B guarantees what basic bound?
   - A. Exactly r requests in every second
   - B. No burst
   - C. Up to roughly B+r×t over an interval t under its assumptions
   - D. Global order

2. Which identity is strongest for account quotas?
   - A. Any client header
   - B. IP always equals a person
   - C. Random URL parameter
   - D. Authenticated account identity

3. Two isolated regions each spend the full global budget. What is wrong?
   - A. Global budget can be exceeded
   - B. Nothing if both use Redis
   - C. More virtual nodes fix it
   - D. TLS prevents it

4. A slow provider saturates in-flight work despite legal arrival rates. What else may help?
   - A. Larger request bodies
   - B. Concurrency limits and deadlines
   - C. Unlimited retries
   - D. Only a longer fixed window


# Async workflows, retries, and notification delivery — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. An outbox primarily closes which gap?
   - A. Provider delivery to a device
   - B. Local business commit versus durable event intent
   - C. Every cross-service transaction
   - D. All duplicate emails

2. A provider times out after possibly accepting. The outcome is what?
   - A. Definitely failed
   - B. Definitely not sent
   - C. Unknown until reconciled or otherwise resolved
   - D. Always safe to resend through a new provider

3. Backlog B drains at B/(μ−λ) when what holds?
   - A. Always
   - B. μ=λ
   - C. Retries are infinite
   - D. μ>λ under a stable simplified model

4. A useful user-facing notification-delay signal is what?
   - A. Oldest pending work/completion delay
   - B. Only average worker CPU
   - C. Only number of code classes
   - D. Only broker brand


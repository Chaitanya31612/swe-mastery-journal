# One valid adaptation

Business rules belong below the controller. Enforce required task state and ownership in the use case or domain layer. HTTP annotations are one input boundary; a worker must validate its inputs too. Use database constraints for rules that must survive concurrency.

**Explain back:** Bind → check → act → reply. What changed in the new condition? What would make your answer fail?

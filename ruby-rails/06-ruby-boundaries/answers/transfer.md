# One valid adaptation

No. MRI does not normally execute multiple Ruby instruction streams in parallel under its VM lock.

More threads may help waiting on I/O, but CPU work may need processes, a different runtime, or less work. Measure throughput and memory with representative synthetic data.

**Explain back:** Catch what you can explain. Test what you can observe.

What changed in the new condition? What would make your answer fail?
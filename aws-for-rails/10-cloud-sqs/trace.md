## Trace the execution

Send → visible → receive → temporarily invisible → DB effect → delete. Crash after DB commit but before delete leads to repetition, which a unique event/command identity must tolerate.

DLQ means quarantined for investigation, not successfully processed. Redrive after a repair needs a repeat-safe consumer and an understanding of ordering consequences.
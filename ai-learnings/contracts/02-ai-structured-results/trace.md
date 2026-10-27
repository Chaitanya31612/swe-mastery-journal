## Follow the execution

Provider bytes → JSON parse → schema validation → domain validation → authorization → execution or fallback. Put each rejection on a trace with a safe error code.

Do not include raw sensitive payloads in logs just to diagnose formatting.
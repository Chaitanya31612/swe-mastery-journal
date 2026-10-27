## Understand

Multimodal models can accept supported combinations of text, images, audio or other inputs. They expand what can be interpreted, not what may be trusted.

A scanned form, screenshot or recording can contain missing context, extraction errors or injected instructions.

Preserve provenance through parsing: page, region, timestamp, speaker/segment where relevant, and source version. A document answer may depend on table layout, units, handwriting or an attachment that was not included.

Treat OCR/transcription and interpretation as separate stages and evaluate their errors independently.

Bound input size/cost, validate file types with robust handling, control storage/access, and expose uncertain/unreadable states. For important structured values, validate against authoritative records or a human review process.

Never silently “correct” a digit because it looks more plausible to the model.
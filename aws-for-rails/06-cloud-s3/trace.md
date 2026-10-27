## Trace the execution

User requests attachment → Rails authorizes record → app issues allowed key/URL → browser uploads bytes → app verifies completion and saves metadata → later read rechecks access before issuing a download.

Test the crash between upload and metadata save. Orphan cleanup must distinguish abandoned objects from live references. For immediate revocation needs, consider the lifetime of already issued URLs.

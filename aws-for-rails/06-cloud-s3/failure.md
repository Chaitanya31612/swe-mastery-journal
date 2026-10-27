## Break it and reason about the repair

A public bucket can bypass Rails permission checks. Reusing a key can replace an existing object according to the operation/versioning contract. A presigned URL should not be logged as harmless metadata.

**Remember:** DB owns permission and meaning. S3 owns bytes.

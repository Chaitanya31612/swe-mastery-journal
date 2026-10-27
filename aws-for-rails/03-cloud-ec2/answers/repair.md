## One valid repair

Store shared objects in S3 or another deliberate shared storage service, retain metadata/permissions in the DB, and avoid instance-local upload assumptions. Test a read from either instance and replacement of one instance.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.

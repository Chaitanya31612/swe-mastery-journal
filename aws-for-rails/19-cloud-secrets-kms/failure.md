## Break it and reason about the repair

Encrypting a secret in Git does not automatically establish safe key ownership. A successful secret fetch does not prove the DB accepts it. Rotation without refresh can cause intermittent failures.

**Remember:** Secret value, key permission, client lifetime, user permission.

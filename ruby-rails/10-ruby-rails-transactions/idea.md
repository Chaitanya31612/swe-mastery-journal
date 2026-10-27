# The idea

Use a service object to name one business action, such as ReserveStock. Use a transaction when its database changes must commit together. A service object by itself supplies no transaction, retry, or permission guarantee.

save returns false when validations fail. save! raises, which can make a failure visible to the transaction boundary. An ordinary false result is not automatically a rollback of earlier successful writes. ActiveRecord::Rollback requests a rollback without propagating like an ordinary error from the transaction block.

after_commit runs after a successful database commit. It avoids publishing from a transaction that later rolls back. It still leaves a gap: the process can crash after commit and before enqueue. A transactional outbox stores delivery intent with the change, then a worker dispatches it.

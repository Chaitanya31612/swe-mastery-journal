# The idea

A transaction groups database changes so they commit or roll back together. It does not automatically group a database write with an email or an external API call.

Spring commonly applies @Transactional through a proxy: a wrapper around the real bean. A call that enters through that proxy can start a transaction. Calling this.otherMethod() inside the object usually skips that proxy. Private methods are also unsuitable boundaries for this common setup.

By default, unchecked exceptions and Error trigger rollback; checked exceptions do not unless configured. A caught exception may not escape to the wrapper at all. Also, two valid transactions can still race. Use a database constraint, conditional update, or appropriate lock for the rule you need.

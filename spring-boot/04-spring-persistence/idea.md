# The idea

JPA maps objects to relational rows. Hibernate is a common implementation. A repository is an access boundary; it does not remove the need to reason about SQL.

An entity loaded inside a persistence context is managed. Changing it can produce an UPDATE when work is flushed. Flush sends SQL; commit makes the transaction durable. They are not the same event. A detached object is no longer tracked by that context.

Associations can hide database work. Reading 20 tasks and then each task.owner.name can issue 21 queries. That is N+1: one list query plus one per item. Choose a fetch plan or a DTO query for this screen. Do not switch every relation to eager loading; that can load a huge graph.

# Ruby · Rails at work

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [Values, names, and surprising mutation](01-ruby-values/README.md): Predict Ruby truthiness and explain when two names share one object.
- 02. [Enumerable: choose the shape of the result](02-ruby-blocks/README.md): Use each, map, select, find, and reduce without hiding side effects.
- 03. [Classes, modules, and method lookup](03-ruby-objects/README.md): Find which method runs before changing an inheritance or mixin chain.
- 04. [Arguments, closures, and return behavior](04-ruby-arguments/README.md): Explain keyword forwarding and the difference between a proc and a lambda.
- 05. [Errors, files, gems, and small tests](06-ruby-boundaries/README.md): Write a reliable boundary around failure and know what a passing Ruby test proves.
- 06. [Rails request: route, scope, params, response](07-ruby-rails-request/README.md): Trace a Rails 4.2 action and protect record ownership at the server.
- 07. [ActiveRecord: relation first, SQL later](08-ruby-rails-queries/README.md): Predict query timing and repair N+1 without loading every association.
- 08. [Validations help users; constraints protect rows](09-ruby-rails-schema/README.md): Choose the right layer for uniqueness and evolve a schema safely.

## Intermediate

- 09. [Read the magic before writing more](05-ruby-metaprogramming/README.md): Explain define_method, dynamic dispatch, and DSLs with an explicit method map.
- 10. [Services, transactions, locks, and callbacks](10-ruby-rails-transactions/README.md): Trace a Rails transaction and explain what after_commit does and does not promise.
- 11. [Sidekiq jobs, retries, and cache freshness](11-ruby-rails-jobs/README.md): Make a job safe to repeat and explain when cached data may be old.
- 12. [Read legacy Rails and prove a safe change](12-ruby-rails-testing/README.md): Map a production-style feature, write behavior tests, and explain a change without copying work code.
- 13. [Rails service objects with a result you can trust](13-ruby-service-contracts/README.md): Define inputs, results, transaction ownership, and error policy for one Rails use case.
- 14. [Multi-tenant scopes and object-level permission](14-ruby-tenant-boundaries/README.md): Keep workspace identity in reads, writes, caches, jobs, and tests.
- 15. [Rails queries: indexes, batching, and bounded reports](15-ruby-query-plans/README.md): Choose SQL work, Ruby work, and batching with attention to memory and business semantics.
- 16. [Time zones, schedules, and jobs that run twice](16-ruby-time-jobs/README.md): Separate an instant, a local calendar rule, a schedule trigger, and a unique business run.
- 17. [Refactor callback-heavy Rails without changing behavior accidentally](17-ruby-callback-refactor/README.md): Map hidden effects, move orchestration carefully, and keep a regression timeline.
- 18. [Compatibility and boundary tests for a legacy Rails stack](18-ruby-compatibility-tests/README.md): Plan a small change or upgrade using version-specific tests rather than broad rewrites.

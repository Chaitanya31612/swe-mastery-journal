# A small example

```ruby
tasks = Task.where(done: false).order(:id).limit(20)
# No iteration yet: this is a relation.
tasks = tasks.preload(:owner)
rows = tasks.map { |task| [task.id, task.owner.name] }

ids = Task.where(done: false).limit(20).pluck(:id)
```
Use synthetic data and SQL instrumentation in a separate sandbox. Do not paste production rows into notes or AI chat.

The precise number of queries depends on association shape and query strategy.
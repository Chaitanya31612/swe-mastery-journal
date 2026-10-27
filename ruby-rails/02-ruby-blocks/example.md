# A small example

```ruby
tasks = [{id: 1, done: false}, {id: 2, done: true}]
ids = tasks.map { |task| task[:id] }           # [1, 2]
open_tasks = tasks.select { |task| !task[:done] }
first_done = tasks.find { |task| task[:done] } # the second hash
count = tasks.reduce(0) { |n, task| n + (task[:done] ? 1 : 0) }

def with_note
  puts "before"
  yield "task-1"
  puts "after"
end
with_note { |id| puts id }
```

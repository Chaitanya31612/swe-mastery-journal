# A small example

```ruby
class TaskPresenter
  LABELS = { open: "Open", done: "Done" }.freeze
  LABELS.each do |state, text|
    define_method("#{state}_label") { text }
  end
end
p TaskPresenter.new.done_label # "Done"

COMMANDS = { "preview" => -> { "preview only" } }.freeze
def run_command(name)
  command = COMMANDS.fetch(name) { raise ArgumentError, "unknown command" }
  command.call
end
```

Use obj.method(:done_label).source_location and .owner to locate the definition. This is a small internal DSL: a limited language for declaring labels.

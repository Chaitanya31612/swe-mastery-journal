# A small example

```ruby
# Rails/Sidekiq teaching fragment, not the standalone Ruby lab.
class TaskReceiptWorker
  include Sidekiq::Worker
  sidekiq_options retry: 5
  def perform(task_id, event_key)
    task = Task.find_by(id: task_id)
    return unless task
    ReceiptSender.new.call(task, event_key)
  end
end
# After a deliberate commit/outbox boundary:
# TaskReceiptWorker.perform_async(task.id, event_key)
```
ReceiptSender must define duplicate handling. A unique local sent row alone cannot atomically prove a remote send happened.

Use a provider key or reconciliation for that gap.
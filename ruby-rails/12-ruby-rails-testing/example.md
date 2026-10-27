# A small example

```ruby
# A small ordinary Ruby service can be tested without Rails.
class CompleteTask
  def initialize(repository)
    @repository = repository
  end
  def call(id)
    task = @repository.fetch(id)
    return :already_done if task[:done]
    @repository.mark_done(id)
    :completed
  end
end
```
This unit seam teaches behavior, not transaction safety. The capstone also needs database and request tests in a separate training app.

Use synthetic rows. Never run course commands in the work repository.
# A small example

```ruby
# Rails 4.2 style.
class Task < ActiveRecord::Base
  validates :key, presence: true,
    uniqueness: { scope: :workspace_id }
end
class AddTaskKeyIndex < ActiveRecord::Migration
  def change
    add_index :tasks, [:workspace_id, :key], unique: true
  end
end
```
Before creating the index, check and resolve existing duplicates in a safe migration plan.

For large production tables, study PostgreSQL concurrent index creation and the Rails 4.2 transaction settings; the short fragment above is a teaching migration, not an online rollout recipe.
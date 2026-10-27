# A small example

```ruby
# Teaching fragments; authentication and associations must be configured.
class TasksController < ApplicationController
  before_action :require_user
  def update
    task = current_user.tasks.find(params[:id])
    if task.update(task_params)
      render json: { id: task.id, title: task.title }
    else
      render json: { errors: task.errors.full_messages }, status: 422
    end
  end
  private
  def task_params
    params.require(:task).permit(:title)
  end
end
```

The example assumes current_user is trustworthy and tasks is the allowed ownership scope. A real app may use a policy/ability layer as well.

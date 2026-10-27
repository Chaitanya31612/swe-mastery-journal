## Follow a concrete example

```ruby
workspace = current_user.workspaces.find(params[:workspace_id])
ticket = workspace.tickets.find(params[:id])
authorize! :update, ticket # example policy integration, if configured
ticket.update!(params.require(:ticket).permit(:title))

# Cache context is part of the key, not permission by itself.
key = "workspace:#{workspace.id}:ticket:#{ticket.id}:v#{ticket.lock_version}"
```

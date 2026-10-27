# The idea

Start a legacy feature investigation at its entry point. Find the route, controller action, service, model/query, callbacks, worker, and response presenter.

Draw only the path relevant to the reported behavior. Search for callers before changing a method contract.

Rails 4.2 uses classic autoloading. File paths, constant names, and development reload behavior matter.

Modern Zeitwerk rules cannot be pasted in as if they already run here. Concerns can install callbacks; a method body alone may not show the whole action.

Use model tests for domain rules, request/controller tests for the HTTP boundary, and job/service tests for failure and duplicate handling.

The course examples are new task-tracker examples informed by broad patterns such as services, concerns, SQL boundaries, and workers.

No private work code or real data belongs in these lessons or AI chat.
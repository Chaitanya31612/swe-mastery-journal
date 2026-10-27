## Understand the idea

Authentication answers who the caller is. A tenant/workspace scope answers which records belong to the current context.

Authorization answers which actions are allowed on those records. None replaces the others.

An ID is not proof of access. Load through an allowed scope or enforce a policy before a write.

Strong parameters limit fields; they do not establish row access. A job argument must also identify and validate the intended tenant/context.

Caches and analytics are data boundaries too. A cache key missing workspace identity can serve another workspace’s result.

Default scopes can hide tenant filtering but are easy to bypass accidentally; make important scope assumptions visible and test them.
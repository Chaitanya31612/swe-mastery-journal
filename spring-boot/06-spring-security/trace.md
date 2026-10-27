# Follow the execution

Follow a request with no credentials: the security entry point decides how to challenge or redirect. Follow a valid user requesting somebody else’s task: authentication can succeed while authorization fails.

For API tests, assert response status and that no write occurred. Check session cookie settings, CSRF expectations, and explicit allowed origins separately. Keep secrets and token contents out of logs.

# The idea

Authentication identifies the caller. Authorization decides whether that caller may access this specific task.

A logged-in user can still be forbidden from editing another user’s data.

Spring Security usually runs in a servlet filter chain before controller handling. It can authenticate a session or bearer token and attach a security context.

Route rules are a first gate. The service still needs object-level rules when it can be called from another route or job.

CORS controls which browser origins can read responses. It is not an ownership check.

CSRF protects cookie-authenticated actions from unwanted cross-site requests. Do not disable it merely because the endpoint uses JSON.

Decide from the authentication mechanism and browser threat model.
## Trace the execution

Browser request → edge key lookup → cached response or origin fetch → response headers → app behavior. Trace a permission change and decide whether an already cached/signed response remains usable.

For deployment, keep the HTML shell and referenced asset versions compatible. A stale shell pointing to removed files can break the app even when the new bundle is correct.
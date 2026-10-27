# One valid repair

Check the startup log for the listening port, then call 8081/ping. Check that the controller package is below the application package and that the mapping is GET /ping.

Separate a connection failure from an HTTP 404.

**How to check:** A 404 means a server handled the request but did not find that resource. Inspect routing and package discovery before changing memory or transactions.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
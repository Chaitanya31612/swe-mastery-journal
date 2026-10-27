# Follow the execution

Write the synchronous lines first: A and D. Then drain the promise callback: C.

Then the timer task can run: B.

For search, label each request with a number. Only the latest number may publish rows.

Also guard loading/error updates; a stale failure must not replace the current success. Encode user input when putting it into a URL.
# The idea

In the App Router, Server Components can read server-only data without shipping that code to the browser. Client Components support hooks and browser interaction. A use client boundary marks a client module graph; it does not mean that component never participates in server-rendered HTML.

Pass serializable data across the server/client boundary. Keep secrets and database clients on the server. Put the interactive leaf near the button rather than moving the entire page into the client by habit.

Next.js caching behavior changes across versions. Record the version and make freshness choices explicit. Browser/router cache, server data cache, rendered output, and the backing database are different layers. A refresh of one does not automatically invalidate every other one.

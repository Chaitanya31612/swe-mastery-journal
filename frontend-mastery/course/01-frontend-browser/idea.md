# The idea

The browser turns a URL into a request, receives HTML, builds a DOM tree, loads CSS and JavaScript, and paints pixels. JavaScript can change the DOM later. Layout calculates geometry. Paint draws visible styles. These are different costs.

In a client-routed app, clicking a link may update browser history and UI without requesting a whole new document. Refreshing that URL is still a server request, so the server needs an appropriate route fallback. A blank page after refresh can be a serving/configuration bug rather than a component bug.

HTML from server rendering can appear before client JavaScript is interactive. Hydration connects client behavior to that initial markup. Initial client output must agree with the server output where hydration expects a match.

# Start with this

The browser turns a URL into a page you can see and use.

Think of it as a few separate jobs.

```text
Request a URL → receive HTML → build the DOM
                                  ↓
                     use CSS to calculate layout
                                  ↓
                         paint visible pixels
```

The DOM is the browser’s tree of page elements. JavaScript can change that tree later.

**Layout** finds sizes and positions. **Paint** draws visible styles.

Changing the page can trigger more of this work. Different changes have different costs.

## A small example

You click a link in a Vue app. The app may change the URL and screen without loading a new HTML document.

Now refresh that same URL. The browser makes a new server request.

The server must know how to return the app for that route. A blank page after refresh may be a server setup problem.

## Server-rendered pages

A server can send HTML before browser JavaScript is ready.

**Hydration** connects that existing HTML to the app’s browser behavior.

The initial browser output must match the server output where hydration expects it to match.

## Remember

“Show HTML,” “run JavaScript,” “calculate layout,” and “paint pixels” are different steps.

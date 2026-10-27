# Follow the execution

Trace document request → HTML parsing → CSS/layout → script → UI change. Then trace a client navigation separately.

The network requests and work can differ.

For a slow page, determine whether the wait is server response time, asset loading, script execution, layout, or a later API call. A single “loading” label hides several possible causes.
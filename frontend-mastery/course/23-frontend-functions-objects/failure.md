## Break it and reason about the repair

A callback can keep large objects alive after the screen closes. A detached method can lose this.

Checking obj[key] alone can confuse absent values with inherited properties or valid falsey values.

**Remember:** Creation decides scope. Calling decides normal this.
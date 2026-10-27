# Follow the execution

1. The JVM calls main. Boot builds the context.
2. Component scanning finds PingController. MVC records its /ping mapping.
3. The server listens on the configured port. A request reaches the mapped method.
4. The method returns text. MVC writes the HTTP response.

Command-line properties override application.properties for this simple case. Profiles select environment-specific settings; they are not a place to commit secrets. Use the condition report (--debug) to see why a default was applied.

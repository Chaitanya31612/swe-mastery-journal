## Understand the idea

Configuration changes behavior without changing the application’s source. That makes it powerful and easy to misunderstand. A value may come from a file, profile, environment variable, command line, or remote source. Record the effective value and its source without logging secrets.

Group related settings with typed configuration rather than scattering string lookups. Validate required URLs, limits, and durations at startup. A service that starts with an invalid payment endpoint can fail much later in a confusing place.

Profiles select groups of behavior; they are not a permission system or a secret store. Prefer workload identity for cloud access and explicit secret injection. Test the production-like configuration graph separately from pure business logic.

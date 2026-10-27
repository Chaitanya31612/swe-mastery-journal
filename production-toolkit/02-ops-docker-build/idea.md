## Understand the idea

A Dockerfile records image construction. Layer caching can speed repeated builds when stable dependency steps occur before frequently changing app files. A .dockerignore keeps unnecessary/private content out of the build context.

Use a deliberately selected base and dependency lockfile. Multi-stage builds can keep compilers out of the runtime image. Run the app with a non-root user when its runtime needs permit. Pass secrets through supported build/runtime mechanisms rather than copying them into layers.

The main process needs signal handling and graceful shutdown. Shell wrappers can change how signals reach the app. Use an exec-style command or an entrypoint that execs the application. Image size matters, but a tiny unmaintainable image is not the goal.

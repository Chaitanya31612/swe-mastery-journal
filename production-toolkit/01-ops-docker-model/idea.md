## Understand the idea

An image is a packaged filesystem/configuration template. A container is a running or stopped instance with its own writable layer. It runs processes using the host kernel’s container facilities; it is not automatically a whole independent virtual machine.

Stopping a container is different from replacing/removing it. Important state should live in a deliberately managed volume or external service, not accidentally in the writable layer. A bind mount connects a host path; a named volume has a separate lifecycle.

Use Docker to make runtime dependencies and process startup reproducible. It does not fix application permissions, data backups, or unsafe code. Learn the process, filesystem, network, and identity boundaries separately.

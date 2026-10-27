# Start with three things

- **Image:** packaged files and settings used to start a container.
- **Container:** an instance of that image, with its own writable layer.
- **Volume:** storage with a lifecycle you manage separately.

```text
Image → start → container → application process
                   ↓
          important data goes to managed storage
```

A container runs processes using the host kernel’s container features.

It is not automatically a separate virtual machine with its own kernel.

## A small example

Write a file inside a container. Stopping that container does not mean you removed it.

Replace the container, and that file may disappear with the old writable layer.

Put important state in a managed volume or an external service.

## Two ways to attach storage

A **bind mount** connects a path on your machine to a path in the container.

A **named volume** has a separate lifecycle managed through Docker.

Know which one you are using before you remove a container.

## Remember

Docker helps repeat the same environment. You still need permissions, backups, and correct application code.

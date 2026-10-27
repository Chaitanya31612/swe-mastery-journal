## Follow a concrete example

```sh
# Local training containers only.
docker image inspect ruby:3.3-slim
docker ps --filter label=com.docker.compose.project=learning-event-lab
docker compose -p learning-event-lab ps
docker compose -p learning-event-lab logs --tail=50 web
```

Use the lab compose file from its directory. Do not run cleanup against all containers or volumes on your machine.

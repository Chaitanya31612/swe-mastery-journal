## Follow a concrete example

```yaml
name: learning-checks
on: [pull_request]
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # training illustration; pin per policy
      - run: echo "Install pinned runtime, then run targeted checks"
```

The example explains structure only. The lab's local checks are not automatically published as a repository workflow or granted cloud access.

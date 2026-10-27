## Follow a concrete example

```text
Source commit → reproducible image build → ECR repository
Tag: git-<revision>
Digest: sha256:<content identity>
Deployment: repository@sha256:<verified digest>
```

CLI login/push commands belong in a controlled pipeline or chosen training session. No registry upload is performed by the course application.

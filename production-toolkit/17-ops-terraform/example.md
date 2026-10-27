## Follow a concrete example

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = var.region }
# Resource examples belong in the selected training account,
# with a reviewed backend, variables, tags, and cleanup plan.
```

This fragment is a configuration shape, not a complete production template.

## Follow a concrete example

```sh
# Read-only checks, using your deliberately configured training profile.
aws sts get-caller-identity --profile learning
aws configure get region --profile learning
```
```ruby
require 'aws-sdk-s3'
s3 = Aws::S3::Client.new(region: ENV.fetch('AWS_REGION'))
# The SDK credential provider chain supplies identity.
# Do not embed access keys in this source.
```
No AWS commands or resource creation run automatically from this course.
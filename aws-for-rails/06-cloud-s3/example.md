## Follow a concrete example

```ruby
require 'aws-sdk-s3'
client = Aws::S3::Client.new(region: ENV.fetch('AWS_REGION'))
signer = Aws::S3::Presigner.new(client: client)
# Authorize the caller and resolve the allowed key on the server first.
url = signer.presigned_url(:get_object,
  bucket: ENV.fetch('ATTACHMENT_BUCKET'),
  key: "workspaces/7/tickets/42/attachment-uuid", expires_in: 300)
```
Use generated object identities, deliberate content rules, and post-upload validation. A successful PUT does not automatically create the correct Rails metadata row.
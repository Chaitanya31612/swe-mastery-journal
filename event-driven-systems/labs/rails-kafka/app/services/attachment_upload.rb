require 'aws-sdk-s3'
class AttachmentUpload
  def initialize(s3:, bucket:)
    @signer = Aws::S3::Presigner.new(client: s3)
    @bucket = bucket
  end

  def call(ticket_id:, attachment_id:)
    # Caller authorizes these IDs first. Browser does not choose arbitrary keys.
    key = "training/tickets/#{Integer(ticket_id)}/#{Integer(attachment_id)}"
    @signer.presigned_url(:put_object, bucket: @bucket, key: key,
                         content_type: 'text/plain', expires_in: 300)
  end
end

## Break it and reason about the repair

latest can mean different images on two machines. Credentials copied into a Docker layer remain in the image even if a later command removes the file.

**Remember:** Build once. Name the bytes.

Deploy those bytes.
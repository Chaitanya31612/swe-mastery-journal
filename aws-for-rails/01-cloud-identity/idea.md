## Understand the idea

An AWS request is made by a principal under a permission context. Human sign-in and application identity should be separate. Use a dedicated training account/profile and temporary credentials. A workload normally receives a role instead of a permanent access key baked into its image.

A role has a trust policy describing who may assume it and permission policies describing allowed actions/resources. Both matter. An explicit deny or an organizational boundary can still block an apparently allowed action. Region and account are part of your context.

Setup path: establish the training account and human SSO/federation flow, configure a named CLI profile, verify caller identity and region, create a narrowly scoped workload role, and test an allowed and denied operation. Budget alerts help notice spend; they are not a hard spending cap.

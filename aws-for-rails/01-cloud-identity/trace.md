## Trace the execution

Human signs in → temporary credentials identify a principal → workload assumes its permitted role → SDK signs a request → AWS evaluates action/resource/context → result or denial.

For an AccessDenied, record the caller ARN, action, resource, and request ID without secrets.

For ECS, distinguish the task role used by app code from the execution role used for platform tasks such as image/secret retrieval.

In EKS, use the supported pod identity mechanism rather than giving every pod the node’s broad privileges.
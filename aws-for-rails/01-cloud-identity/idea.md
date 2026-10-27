# Start with one question: who is making this request?

AWS checks an identity and its permissions before allowing an operation.

That identity is called a **principal**. It might represent a person or an application.

## Keep people and applications separate

Use your own sign-in flow for human access.

Give an application a role with the permissions it needs. Avoid putting a permanent access key inside its container image.

```text
Person or workload → identity → permission checks → allowed AWS action
```

## A role has two important parts

- **Trust policy:** who may use this role?
- **Permission policies:** what actions and resources may it use?

An explicit deny or another policy boundary can still block a request.

The account and region also matter. Check them before you create or change resources.

## A small training exercise

Use a separate training account or profile. Sign in with temporary credentials and check the current identity and region.

Create a narrow workload role. Test one action it allows and one it must deny.

## Remember

“Who are you?” and “What may you do?” are different checks.

Budget alerts help you notice spending. They do not impose a hard spending limit.

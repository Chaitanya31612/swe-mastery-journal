## Break it and reason about the repair

EXPOSE documents a container port; it does not publish it to the host. A running container can contain a failing app. A volume is not itself a tested backup.

**Remember:** Image is the recipe. Container is the instance. Volume is a data decision.

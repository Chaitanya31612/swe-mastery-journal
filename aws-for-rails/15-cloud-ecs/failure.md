## Break it and reason about the repair

An execution role is not automatically the app’s S3 role. Starting more workers can overload the DB/provider. A task repeatedly failing before logs are configured is hard to diagnose.

**Remember:** Image, command, role, network, health, and desired count.

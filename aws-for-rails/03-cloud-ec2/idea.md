## Understand the idea

EC2 gives you virtual machines. You choose an image, instance capacity, network, identity, and storage. You still own operating-system patching, process configuration, application deployment, and much of the recovery plan.

An instance is not the same thing as a persistent data store. EBS volumes have their own lifecycle and zone attachment rules; instance-store data is a different contract. A Rails app should not treat its local upload directory as shared storage across several instances.

Training setup: select a deliberate image/type, attach a narrow instance role, use controlled management access, configure security groups, supervise the app process, send logs off the machine, and test replacing the instance. Keep the database and uploads in services with explicit persistence/backup policies.

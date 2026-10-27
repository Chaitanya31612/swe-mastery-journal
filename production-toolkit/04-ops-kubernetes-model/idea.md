## Understand the idea

Docker packages/runs containers. Kubernetes coordinates desired workloads through an API and controllers. It can use compatible container runtimes; Docker Engine is not a required node runtime for every cluster.

A Pod groups containers that share a lifecycle/network context. A Deployment manages a ReplicaSet and replaceable Pods for suitable workloads. You usually change the desired specification rather than manually repairing a particular pod.

Requests/limits, probes, identity, configuration, and storage affect whether a workload can run usefully. Kubernetes does not know your business transaction rule. A replacement pod can repeat work if the job/consumer boundary is not designed for it.

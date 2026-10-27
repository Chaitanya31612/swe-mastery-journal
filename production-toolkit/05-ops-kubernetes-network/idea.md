## Understand the idea

Pods can be replaced and their addresses can change. A Service gives a stable access abstraction for matching endpoints. Selectors connect the Service to labelled Pods; a spelling mismatch can leave no endpoints.

Ingress or Gateway-related resources describe external routing under a selected controller implementation. Defining an Ingress object does not install every required controller or cloud load balancer. The exact controller’s contract matters.

Map DNS, ports, targetPort, ready endpoints, network policy, and app listener separately. Inside a Pod, localhost refers to its network namespace. Reaching a peer service uses the service name, not the browser’s public URL by habit.

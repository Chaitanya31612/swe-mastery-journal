## Understand the idea

An ALB accepts HTTP(S) traffic and forwards it according to listeners/rules to target groups. The target group knows where application targets live and how health is checked. A listening app port alone does not prove the app should receive traffic.

TLS termination, forwarded headers, idle timeouts, and target health affect Rails behavior. Configure trusted proxy/host handling deliberately. A bad redirect rule can create an HTTPS loop when the app misinterprets the original scheme.

Setup: create the ALB in suitable subnets, attach an allowed ingress group, add an HTTPS listener/certificate, create a target group with the correct app port and readiness path, allow only the ALB-to-app path, register targets, and observe a request and a failed target.

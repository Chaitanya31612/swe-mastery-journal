## Understand the idea

DNS resolves a name to a destination. It does not forward each HTTP request through a Rails controller.

Route 53 can manage DNS records and health/routing policies. Cached answers mean a record change is not an instantaneous global traffic switch.

TLS certificates connect a name to a trusted identity under certificate rules. ACM can manage supported certificates, but you still configure validation and attach the certificate to the right service.

Services can have specific certificate-region requirements; verify those for ALB versus CloudFront.

Setup: own/control the domain, establish the hosted zone and registrar delegation, create/validate the certificate, attach it to the selected listener/distribution, create the deliberate alias/record, and test DNS plus HTTPS separately.

Keep domain renewal and validation records in the ownership map.
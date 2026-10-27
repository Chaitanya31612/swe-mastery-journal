## Understand the idea

An email integration has several states: saved intent, attempted request, provider acceptance, recipient-server delivery, bounce, suppression, and user interaction.

The API accepting a request does not prove the person received or read it.

Use a narrow adapter and store a logical notification identity. Authenticate the sending domain and configure the selected provider’s required settings.

Keep secrets out of code and validate webhook signatures/replay policy using the provider’s supported mechanism.

Setup: choose a training/sandbox mode, verify sender/domain configuration, scope the API credential, define templates and minimal data, add signed event-webhook handling, and test accepted, rejected, bounced, duplicate-event, and timeout cases.

This course sends no real email.
## Understand the idea

Pendo supports product analytics/guidance capabilities, including configured Track Events. Define what an event means before instrumenting it.

A clicked button, an accepted request, and a completed business action are different events.

Choose stable names and a minimal property schema. A support app might record TicketAssignmentCompleted with method and outcome category, rather than every typed title or description.

Visitor/account association and data collection settings must match the product’s privacy/access policy.

Setup: choose a training application/configuration, establish identity and collection policy, instrument one deliberate event after the relevant boundary, verify it arrives, and compare it with the actual business outcome.

Keep server-side secrets out of the browser and source. This course sends no analytics to Pendo.
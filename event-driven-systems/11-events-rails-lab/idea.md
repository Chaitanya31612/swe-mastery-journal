## Understand the idea

The local lab uses fresh support-ticket code. It borrows broad production patterns—service objects, transactions, workers, and projections—without copying private application code or data. It uses Ruby 3.3/Rails 7.2 with a pinned Kafka client; that is separate from the Ruby 2.7/Rails 4.2 work baseline.

Read in this order: routes/controller, CompleteTicket service, migrations/models, envelope builder, Kafka producer adapter, outbox dispatcher, reporting projector, consumer loop, and tests. Each file owns one boundary. Infrastructure/config files explain how the processes find one another.

Run the smoke script and failure drills with synthetic data. Do not merely watch logs scroll. Predict the ticket, outbox, topic, inbox, and projection state at each stop point. The app contains no real email, analytics, or cloud credentials.

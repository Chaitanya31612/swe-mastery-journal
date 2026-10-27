# Versions and reading map

## Work-oriented Ruby/Rails baseline

Ruby 2.7.8, Rails 4.2.11.3 (a fork), Sidekiq 5.2, PostgreSQL, and Vue 2.6 are the reference context. A fork may differ from upstream guides. Verify behavior in an authorized isolated project test environment when doing real work; these examples do not prove the fork’s exact behavior.

Rails 4.2 uses classic autoloading, ActiveRecord::Base model inheritance, require/permit strong parameters, and older association defaults. Do not silently substitute Zeitwerk, ApplicationRecord, params.expect, modern enqueue-after-transaction APIs, or current Sidekiq::Job syntax. Ruby 2.7 keyword warnings matter for Ruby 3 migration. Vue 2 property-addition limits differ from Vue 3 proxies.

## The three books

- The Ruby Programming Language (2008): data/objects in ch. 3, expressions/control in ch. 4–5, methods/blocks in ch. 6, classes/modules in ch. 7, reflection in ch. 8, platform/environment in ch. 9–10.
- Eloquent Ruby (2011): style/control/collections in ch. 1–6, modules in ch. 16, blocks in ch. 17–20, dynamic behavior in ch. 21–27, gems/testing/runtime in ch. 28–30.
- Metaprogramming Ruby, 2nd Edition (2014): Monday object model, Tuesday methods, Wednesday blocks, Thursday classes, Friday code generation; the Rails tour shows ActiveRecord, concerns, and hooks. alias_method_chain is historical reading, not a new-code recommendation.

These books informed the sequence and concepts. The explanations and task examples are original. No book scans or lengthy extracts are bundled. Page numbers vary by edition; chapter/topic names are the stable guide.

## Spring and frontend

The Java sandbox pins Java 21 and Spring Boot 4.0.3 for reproducibility. That is a teaching baseline, not a claim it is the newest release. Boot 4 uses Jakarta namespaces and changed some test packages from Boot 3. Read docs for the pinned version when copying imports. H2 proves a small training path; PostgreSQL concurrency and constraints need PostgreSQL tests.

Frontend examples state Vue 2/3 and React/Next boundaries explicitly. Next cache defaults vary across releases: name the installed version and chosen policy before relying on behavior. Existing staff notes are optional depth, not extra prerequisite reading before every exercise.


## October 2026 expansion

The new chapters distinguish Beginner from Intermediate. Official references are attached to each module. They cover framework behavior, service setup, operating limits, UX/accessibility, and tool-specific failure boundaries. The examples are original teaching examples. Product behavior and cloud prices can change; use the linked service documentation for the selected region/version before a real setup.

- Vue lessons and lab: Vue 3.5.25; work Vue 2 behavior is labelled separately.
- Spring training app: Java 21 and Spring Boot 4.0.3. Spring examples target the module's stated setup.
- Event lab: Ruby 3.3.6, Rails 7.2.2.2, rdkafka 0.20.0, PostgreSQL 16.6, Kafka 4.1.0 in KRaft mode. This is an isolated modern training environment, not a work upgrade.
- AWS examples: SDK for Ruby v3. Local adapter tests use stub_responses. Cloud setup is an explicit optional workbook; no cloud service is provisioned by the app.
- Redis lab: Redis 7.4.2, standalone local topology. It does not establish multi-node failover guarantees.
- Container images are pinned learning baselines. Check maintenance/security support before using them for a real deployment.

The Kafka course distinguishes producer retry idempotence, business event identity, group offsets, DB inbox/projection transactions, and external effects. It does not promise end-to-end exactly-once behavior across all systems. The UX laws are reasoning tools with assumptions; accessibility and observed task performance need their own checks.

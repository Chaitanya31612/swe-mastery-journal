from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
index=json.loads((ROOT/'software-learnings/course-index.json').read_text())
entries={e['id']:ROOT/e['directory'] for e in index['modules']}
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Make the main frontend route match the learner's daily Vue work.
t=next(t for t in index['tracks'] if t['id']=='frontend')
t.update(title='Frontend · JavaScript & Vue 3',description='Build JavaScript and CSS foundations. Follow Vue 3 state, requests, forms, rendering, and tests. React and Next.js remain comparison chapters.',version='JavaScript and TypeScript · CSS · Vue 3.5 · Vue 2 compatibility notes')
original_frontend={'frontend-browser','frontend-runtime','frontend-state','frontend-react','frontend-vue','frontend-experience','frontend-next','frontend-capstone'}
for id,folder in entries.items():
 if id.startswith('frontend-') and id not in original_frontend:
  p=folder/'module.json';m=json.loads(p.read_text());m['version']='Modern JavaScript / TypeScript · Vue 3.5 where applicable · browser APIs';save(p,m)
# One authoritative multi-file Rails lab. AWS view selects the adapter subset.
rails=ROOT/'event-driven-systems/labs/rails-kafka'
(rails/'README.aws.md').write_text((ROOT/'aws-for-rails/labs/rails-adapters/README.md').read_text())
files=['README.md','compose.yaml','Dockerfile','Gemfile','Gemfile.lock','config/routes.rb','app/controllers/tickets_controller.rb','app/services/complete_ticket.rb','app/services/ticket_event.rb','app/services/outbox_dispatcher.rb','app/services/kafka_publisher.rb','app/services/reporting_consumer.rb','app/services/apply_reporting_event.rb','db/migrate/20261021000100_create_event_learning.rb','app/models/ticket.rb','app/models/outbox_event.rb','app/models/inbox_event.rb','app/models/reporting_projection.rb','bin/dispatch.rb','bin/consume.rb','test/event_flow_test.rb','test/tickets_api_test.rb','smoke.py','config/application.rb','config/database.yml','config/environment.rb','config/boot.rb','config/environments/development.rb','config/environments/test.rb','app/controllers/application_controller.rb','app/models/application_record.rb','bin/rails','db/seeds.rb','Rakefile','config.ru','test/test_helper.rb','app/services/attachment_upload.rb','app/services/queue_worker.rb','test/aws_adapters_test.rb']
labs=[{'id':'rails-kafka','title':'Follow a Rails event across files','version':'Ruby 3.3.6 · Rails 7.2.2.2 · Kafka 4.1.0 · rdkafka 0.20.0 · PostgreSQL 16.6','directory':str(rails.relative_to(ROOT)),'files':files},
 {'id':'aws-rails','title':'Rails on AWS · setup and adapter seams','version':'AWS SDK for Ruby v3 · local stubbed checks + optional cloud setup workbook','directory':str(rails.relative_to(ROOT)),'guide':'README.aws.md','files':['README.aws.md','app/services/attachment_upload.rb','app/services/queue_worker.rb','test/aws_adapters_test.rb','Gemfile','Gemfile.lock','compose.yaml']},
 {'id':'redis','title':'Redis · data, expiry, atomic updates, and leases','version':'Redis 7.4.2 · Python standard-library RESP client','directory':'production-toolkit/labs/redis','files':['README.md','compose.yaml','lab.py']},
 {'id':'vue-workspace','title':'Vue 3 · async requests and independent edit drafts','version':'Vue 3.5.25 · Vite 7.3.1 · Vitest 4.1.11 · synthetic data','directory':'frontend-mastery/labs/vue-ticket-workspace','files':['README.md','src/TicketWorkspace.vue','src/useTicketSearch.ts','src/api.ts','src/TicketWorkspace.test.ts','src/main.ts','vite.config.ts','package.json','index.html']}]
save(ROOT/'software-learnings/labs.json',labs)
frontend_order=['frontend-browser','frontend-data-contracts','frontend-functions-objects','frontend-runtime','frontend-typescript','frontend-css-layout','frontend-state','frontend-vue-components','frontend-vue','frontend-experience','frontend-async-coordination','frontend-web-platform','frontend-css-systems','frontend-dom-lifecycle','frontend-vue-reactivity','frontend-vue-composables','frontend-vue-async','frontend-vue-routing-store','frontend-vue-forms','frontend-rendering-budget','frontend-vue-performance','frontend-vue-testing','frontend-browser-security','frontend-react','frontend-next','frontend-capstone','frontend-delivery-capstone']
for id in ['frontend-vue-components','frontend-vue-composables','frontend-vue-async','frontend-vue-forms','frontend-vue-testing','frontend-delivery-capstone']:
 p=entries[id]/'module.json';m=json.loads(p.read_text());m['lab']='vue-workspace';save(p,m)
# Concrete diagrams supplement the simple memory paths.
diagrams={
'cloud-architecture':'''flowchart TD
 Browser --> DNS[Route 53 and TLS]
 DNS --> CDN[CloudFront]
 CDN --> ALB[Application Load Balancer]
 ALB --> Web[Private Rails web tasks]
 Browser -->|signed upload| S3[Private S3 objects]
 Web --> DB[(RDS PostgreSQL)]
 Web --> Redis[(ElastiCache Redis)]
 Web --> SQS[SQS jobs]
 SQS --> Worker[Rails worker tasks]
 Web --> Outbox[(Transactional outbox)]
 Outbox --> Relay[Dispatcher or CDC]
 Relay --> MSK[MSK Kafka when replay is needed]
 MSK --> Reports[Reporting consumer]
 Web -. task role .-> IAM[IAM and Secrets Manager]
 Web -. signals .-> Observe[CloudWatch or Datadog]
 Worker -. signals .-> Observe''',
'ops-toolkit-capstone':'''flowchart TD
 Git[Git review] --> CI[GitHub Actions]
 CI --> Image[Docker image in ECR]
 TF[Terraform] --> Infra[Network and managed services]
 Image --> Runtime{Choose a runtime}
 Runtime --> ECS[ECS service]
 Runtime --> EKS[EKS Kubernetes service]
 ECS --> Rails[Rails web and workers]
 EKS --> Rails
 Rails --> Pool[Optional PgBouncer]
 Pool --> DB[(PostgreSQL)]
 Rails --> Redis[(Redis - deliberate purpose)]
 DB --> CDC[Debezium OR outbox dispatcher]
 CDC --> Kafka[Kafka retained log]
 Kafka --> Projection[Reporting projection]
 Projection --> Store[(Postgres or query-driven Cassandra)]
 Rails --> Email[SendGrid delivery adapter]
 Cron[One scheduler with job identity] --> Rails
 Rails -. OTel signals .-> Obs[Datadog or Prometheus and Grafana]
 Browser[Browser workflow] -. safe product events .-> Pendo[Pendo]
 Flags[Feature flag lifecycle] --> Rails''',
'events-layers':'''flowchart TD
 Producer[Producer batches and key partitioner] --> Leader[Partition leader broker]
 Leader --> Log[(Partition log segments)]
 Leader --> Followers[Follower replicas]
 Followers --> Ack[ISR and acknowledgment policy]
 Ack --> Producer
 Log --> Consumer[Consumer fetch and local position]
 Consumer --> Effect[(Application DB effect)]
 Effect --> Commit[Group committed next offset]
 Controller[KRaft controller quorum] -. metadata and leader decisions .-> Leader
 Commit -. restart position .-> Consumer''',
'events-outbox':'''sequenceDiagram
 participant R as Rails use case
 participant DB as Business database
 participant D as Dispatcher
 participant K as Kafka
 R->>DB: BEGIN - state and outbox row
 DB-->>R: COMMIT
 D->>DB: Read pending row
 D->>K: Publish stable event ID
 K-->>D: Delivery acknowledged
 Note over D,K: Crash here can repeat publication
 D->>DB: Mark row published''',
'events-inbox':'''sequenceDiagram
 participant K as Kafka partition
 participant C as Consumer
 participant DB as Reporting database
 K->>C: Event at offset N
 C->>DB: BEGIN - insert unique inbox ID
 C->>DB: Apply reporting effect
 DB-->>C: COMMIT together
 Note over C,DB: Crash here replays - inbox skips repeat
 C->>K: Commit next offset N+1''',
'frontend-vue-async':'''sequenceDiagram
 participant UI as Search UI
 participant A as Request A
 participant B as Request B
 UI->>A: Search old text
 UI->>UI: New query invalidates A owner
 UI->>B: Search new text
 B-->>UI: New result accepted
 A-->>UI: Old success or error ignored
 Note over UI,B: Guard rows, errors, and loading''',
'ops-debezium':'''flowchart LR
 Rails --> TX[DB transaction]
 TX --> Outbox[(Outbox table)]
 TX --> WAL[(Postgres WAL)]
 WAL --> Slot[Replication slot and connector offset]
 Slot --> CDC[Debezium connector]
 CDC --> Router[Outbox event router]
 Router --> Kafka[Kafka topic]
 Slot -. stalled connector retains WAL .-> Disk[Monitor disk and lag]''',
'ux-feedback':'''flowchart TD
 Action[User chooses Save] --> Pending[Saving - keep ownership clear]
 Pending --> Result{Known outcome?}
 Result -->|success| Saved[Show saved state]
 Result -->|validation error| Repair[Explain field and repair]
 Result -->|unknown network outcome| Reconcile[Check status before retrying a write]
 Repair --> Action
 Reconcile --> Result''',
'ops-kubernetes-model':'''flowchart TD
 Image[Docker-built OCI image] --> Registry[Image registry]
 Registry --> Deployment[Deployment desired replicas]
 Deployment --> RS[ReplicaSet]
 RS --> Pod[Pod - containers share network and volumes]
 Scheduler[Scheduler] --> Node[Worker node]
 Pod --> Node
 Node --> Runtime[Container runtime runs image]
 Service[Service stable endpoint] --> Ready[Ready Pod endpoints]
 Ready --> Pod
 Config[ConfigMap and Secret references] --> Pod'''
}
for id,code in diagrams.items():
 p=entries[id]/'module.json';m=json.loads(p.read_text());m['visuals'][0].update(code=code,title='Follow the real boundaries');save(p,m)
# Order by learning progression, keep stable original identities.
ordered=[]
for t in index['tracks']:
 rows=[e for e in index['modules'] if json.loads((ROOT/e['directory']/'module.json').read_text())['track']==t['id']]
 if t['id']=='frontend':rows.sort(key=lambda e:frontend_order.index(e['id']))
 rows.sort(key=lambda e: 0 if json.loads((ROOT/e['directory']/'module.json').read_text())['level']=='beginner' else 1)
 prev=None
 for n,e in enumerate(rows,1):
  p=ROOT/e['directory']/'module.json';m=json.loads(p.read_text());m['sequence']=n;m['prerequisite']=prev;prev=m['id'];save(p,m);ordered.append(e)
index['modules']=ordered;save(ROOT/'software-learnings/course-index.json',index)
# The actual failure found by the local smoke becomes a teachable boundary.
p=entries['events-operations']/'failure.md';s=p.read_text();note='''\n\n### A real local-lab failure: stale empty outbox reads\n\nThe first long-running rails runner cached an empty SELECT. New HTTP requests inserted outbox rows, but the dispatcher kept seeing its cached empty result. The live smoke timed out. The repair runs each poll inside ApplicationRecord.uncached. This is separate from Redis caching and Kafka lag. Trace the database query before blaming the broker. The final lab smoke checks actual delivery after a new row is inserted.\n'''
if 'stale empty outbox reads' not in s:p.write_text(s+note)
print('Enriched labs, concrete diagrams, and stable learning order.')

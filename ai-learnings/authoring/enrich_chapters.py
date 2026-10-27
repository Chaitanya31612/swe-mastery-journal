"""Add concrete diagrams and cumulative checks after build_chapters.py. Idempotent."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
index=json.loads((ROOT/'course-index.json').read_text())
modules=[]
for entry in index['modules']:
 folder=ROOT.parent/entry['directory']
 modules.append((folder,json.loads((folder/'module.json').read_text())))
DIAGRAMS={
'ai-boundary':'''flowchart TD
 U[Operator asks: show held parcels] --> I[Model proposes status: held]
 I --> V{Allowed fields and values?}
 V -->|No| F[Keep manual filters available]
 V -->|Yes| S[Actor-scoped Rails query]
 S --> C[Database computes count]
 C --> P[Show facts and labelled interpretation]
 I -. No direct SQL or writes .-> X[Application owns authority]''',
'ai-tokens-context':'''flowchart LR
 I[Instructions] --> B[Finite context budget]
 T[Tool definitions] --> B
 H[Selected conversation history] --> B
 E[Retrieved evidence] --> B
 Q[Current question] --> B
 B --> R[Reserve space for output and provider needs]
 R --> F{Fits?}
 F -->|No| S[Select or shorten evidence and history]
 S --> B
 F -->|Yes| M[Model request]''',
'ai-training-inference':'''flowchart TD
 D[Training examples] --> T[Training computes weight updates]
 T --> W[Saved model weights]
 W --> I[Inference uses these weights]
 P[Prompt and selected context] --> I
 I --> O[Generated output]
 N[New company fact] --> C[Database or retrieved context]
 C --> P
 O -. Not normally a weight update .-> W''',
'ai-attention-generation':'''flowchart TD
 T[Input text] --> K[Token IDs]
 K --> E[Numeric token and position representations]
 E --> A[Repeated attention and feed-forward layers]
 A --> L[Scores for possible next tokens]
 L --> S[Decode one token]
 S --> U[Append token to context]
 U --> A
 S --> X{Stop condition?}
 X -->|Yes| R[Return output]
 X -->|No| U''',
'ai-tool-cycle':'''sequenceDiagram
 participant H as Application host
 participant M as Model
 participant P as Policy and validator
 participant T as Domain tool
 H->>M: Task plus allowed tool schemas
 M-->>H: Proposed tool name and arguments
 H->>P: Validate arguments and current actor
 alt Denied or invalid
 P-->>H: Safe error without hidden data
 else Permitted
 H->>T: Execute bounded operation
 T-->>H: Typed result with source version
 end
 H->>M: Tool result correlated to call ID
 M-->>H: Draft or next proposed call
 H->>H: Enforce total steps, time and spend
''',
'ai-facts-or-documents':'''flowchart TD
 Q[User question] --> D{What truth does it require?}
 D -->|Current count or state| S[Scoped SQL and reviewed rules]
 D -->|Policy explanation| R[Permitted versioned document evidence]
 D -->|Both| B[Join facts and evidence with provenance]
 S --> C[Typed current facts]
 R --> E[Retrieved source excerpts]
 C --> G[Optional generated explanation]
 E --> G
 B --> G
 G --> V[Check supported claims or abstain]
''',
'ai-ingestion':'''flowchart TD
 S[Approved source and access policy] --> E[Extract and normalize]
 E --> C[Split with headings and source IDs]
 C --> B[Embed a complete new source version]
 B --> T[Validate count, errors and permissions]
 T --> P[Publish version atomically]
 P --> R[Retrieve active permitted chunks]
 D[Source deleted or access revoked] --> I[Invalidate chunks, vectors and cached answers]
 I --> R
 T -->|Failure| Q[Keep old valid version or mark unavailable]
''',
'ai-hybrid-ranking':'''flowchart LR
 Q[Question] --> L[Lexical candidates]
 Q --> E[Embedding candidates]
 A[Authenticated scope] --> L
 A --> E
 L --> F[Merge candidates by rank]
 E --> F
 F --> R[Optional reranker]
 R --> P[Recheck access and current source version]
 P --> B[Select diverse evidence within budget]
 B --> G[Answer or missing evidence]
''',
'ai-mcp-map':'''flowchart LR
 U[User] --> H[AI host application]
 H --> M[Model provider]
 H --> C1[MCP client connection A]
 H --> C2[MCP client connection B]
 C1 <-->|MCP messages| S1[Shipment MCP server]
 C2 <-->|MCP messages| S2[Document MCP server]
 S1 --> P1[Application policy and shipment tools]
 S2 --> P2[Permitted documents]
 P1 --> D1[(Shipment database)]
 P2 --> D2[(Document store)]
''',
'ai-mcp-lifecycle':'''sequenceDiagram
 participant H as Host MCP client
 participant S as MCP server
 H->>S: initialize with version and capabilities
 S-->>H: Selected version and server capabilities
 H->>S: notifications/initialized
 H->>S: tools/list
 S-->>H: Tool names and input schemas
 H->>H: Choose whether to expose tools to model
 H->>S: tools/call with request ID and arguments
 S->>S: Validate current actor and object access
 S-->>H: Tool result or error
 H->>H: Correlate result and apply execution budget
''',
'ai-rails-architecture':'''flowchart TD
 U[Operator] --> C[Training assistant controller]
 C --> A[Current actor from identity boundary]
 A --> F[Intent service validates filter proposal]
 F --> DB[(Scoped shipment relation)]
 A --> R[Rules fact builder]
 R --> DB
 R --> V[Minimal verified fact snapshot]
 V --> J[Owned explanation run and job]
 J --> P[Provider adapter]
 P --> E[Explanation result checks]
 E -->|Invalid or unavailable| G[Reviewed rule guidance]
 E -->|Accepted| D[Labelled AI draft]
 G --> UI[Presenter with source version]
 D --> UI
 UI --> U
''',
'ai-jobs-results':'''stateDiagram-v2
 [*] --> queued: persist owned run
 queued --> running: atomic claim
 running --> completed: valid draft
 running --> fallback: provider or validation failure
 running --> unavailable: access or source missing
 completed --> stale: source version changed on read
 fallback --> stale: source version changed on read
 completed --> completed: duplicate completed delivery does nothing
 note right of running
 Local lab has no crash lease recovery.
 Design it before using a durable worker.
 end note
''',
'ai-evaluation-dataset':'''flowchart TD
 T[Task and acceptance criteria] --> D[Labelled synthetic cases]
 D --> S[Split development from held-out evaluation]
 S --> R[Run versioned prompt, model and retrieval]
 R --> C[Deterministic contract and access checks]
 R --> H[Human-reviewed task quality]
 C --> G[Slice metrics and inspect failures]
 H --> G
 G --> P{Meets release gate?}
 P -->|No| F[Repair one failure category]
 F --> R
 P -->|Yes| L[Limited release with monitoring and rollback]
''',
'ai-final-capstone':'''flowchart TD
 U[User task and success criteria] --> T[Truth owners and permitted evidence]
 T --> B[Input, output and tool contracts]
 B --> W{Simplest useful flow?}
 W --> C[Deterministic feature]
 W --> R[Retrieval plus model call]
 W --> A[Bounded agent only if justified]
 C --> V[Validation, failure path and honest UI]
 R --> V
 A --> V
 V --> E[Offline checks plus live model evaluation]
 E --> G[Cost, privacy, latency and release gates]
 G --> O[Limited rollout and rollback]
 O --> D[Delayed transfer problem in a new domain]
'''
}
for folder,m in modules:
 if m['id'] in DIAGRAMS:
  code=DIAGRAMS[m['id']].strip()
  m['visuals'][0]['code']=code
  m['visuals'][1]['code']=code
  m['visuals'][1]['title']='Recap · redraw the full mechanism from memory'
  (folder/'README.md').write_text(f"# {m['title']}\n\n{m['outcome']}\n\nStart with idea.md, then example.md, trace.md and failure.md. Try practice before answers.\n\n```mermaid\n{code}\n```\n\nRemember: **{m['cue']}**\n")
 # Remove old derived checks before regenerating.
 qs=[q for q in json.loads((folder/'quiz.json').read_text()) if not q['id'].startswith('review-')]
 keys={k:v for k,v in json.loads((folder/'answers/quiz.json').read_text()).items() if not k.startswith('review-')}
 m.pop('questions',None)
 (folder/'quiz.json').write_text(json.dumps(qs,indent=2,ensure_ascii=False)+'\n')
 (folder/'answers/quiz.json').write_text(json.dumps(keys,indent=2,ensure_ascii=False)+'\n')
 (folder/'module.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
for track in index['tracks']:
 stage=[item for item in modules if item[1]['track']==track['id']]
 endfolder,end=stage[-1]
 earlier=modules[:-1] if track['id']=='advanced-ai' else stage[:-1]
 questions=json.loads((endfolder/'quiz.json').read_text())
 keys=json.loads((endfolder/'answers/quiz.json').read_text())
 for folder,m in earlier:
  q=json.loads((folder/'quiz.json').read_text())[0]
  answer=json.loads((folder/'answers/quiz.json').read_text())[q['id']]
  key='review-'+m['id']
  questions.append({**q,'id':key,'covers':m['id'],'prompt':f"Revisit {m['title']}: {q['prompt']}"})
  keys[key]=answer
 (endfolder/'quiz.json').write_text(json.dumps(questions,indent=2,ensure_ascii=False)+'\n')
 (endfolder/'answers/quiz.json').write_text(json.dumps(keys,indent=2,ensure_ascii=False)+'\n')
print('Enriched',len(DIAGRAMS),'concrete diagrams; cumulative checks for all eight stages')

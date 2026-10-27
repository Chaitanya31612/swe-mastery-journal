from pathlib import Path
import json
import re
import hashlib
import random

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'software-learnings/course-index.json'
NEW = []
TRACK_DIRS = {'spring':'spring-boot','ruby':'ruby-rails','git':'GIT/course','frontend':'frontend-mastery/course','ux':'user-experience','cloud':'aws-for-rails','ops':'production-toolkit','events':'event-driven-systems'}
NEW_TRACKS = [
 {'id':'ux','title':'UX · Design for understanding','description':'Reason from tasks, perception, access, and evidence. Improve a support workflow one decision at a time.','version':'Web UX · WCAG 2.2 · principles, not magic formulas','hours':0},
 {'id':'cloud','title':'AWS · Run a Rails application','description':'Follow a request, file, job, and secret through AWS. Set up small examples and understand their cost and failure paths.','version':'AWS SDK for Ruby v3 · service-specific setup · no cloud resources created automatically','hours':0},
 {'id':'ops','title':'Production toolkit · Build and operate','description':'Docker, Kubernetes, Redis, observability, delivery, and useful integrations. Learn what each tool adds and what you must still own.','version':'Pinned local examples · version-labelled configuration fragments','hours':0},
 {'id':'events','title':'Event-driven systems · Kafka & Rails','description':'Build a mental model of the log, then follow an outbox event through a real multi-file Rails/Kafka lab.','version':'Kafka 4.1 KRaft · lab Ruby 3.3 / Rails 7.2 · legacy Rails adaptation notes','hours':0},
]

def q(prompt, a, b, c, correct, explanation):
    return dict(prompt=prompt,options=[a,b,c],correctIndex=correct,explanation=explanation)

def chapter(track, slug, title, level, goal, idea, example, walk, failure, repair, fix, transfer, adaptation, questions, cue, steps, sources, *, usecase='', benefits='', drawbacks='', tags=None, lab=None, prerequisite=None):
    assert level in ('beginner','intermediate') and len(questions)>=3
    NEW.append(dict(id=f'{track}-{slug}',track=track,title=title,level=level,outcome=goal,idea=idea,example=example,walk=walk,failure=failure,
      repair=repair,fix=fix,transfer=transfer,adaptation=adaptation,questions=questions,cue=cue,steps=steps,sources=sources,
      useCase=usecase,benefits=benefits,drawbacks=drawbacks,tags=tags or [],lab=lab,prerequisite=prerequisite,hours=2))

VUE='https://vuejs.org/guide/essentials/'
MDN='https://developer.mozilla.org/en-US/docs/Web/'
SPRING='https://docs.spring.io/spring-framework/reference/'
RAILS='https://guides.rubyonrails.org/v4.2/'
AWS='https://docs.aws.amazon.com/'
KAFKA='https://kafka.apache.org/41/'

def write(p, text):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text.strip()+'\n')

def emit():
    manifest=json.loads(INDEX.read_text())
    old_ids={e['id'] for e in manifest['modules']}
    new_ids={m['id'] for m in NEW}
    assert len(new_ids)==len(NEW)
    for track in NEW_TRACKS:
        if not any(t['id']==track['id'] for t in manifest['tracks']):manifest['tracks'].append(track)
    # Preserve the identity, order, lesson text, and progress compatibility of every original module.
    intermediate_original={'spring-persistence','spring-transactions','spring-tests','spring-operate','ruby-metaprogramming','ruby-rails-transactions','ruby-rails-jobs','ruby-rails-testing','git-investigation','frontend-next','frontend-capstone','frontend-react'}
    for entry in manifest['modules']:
        if entry['id'] in new_ids:continue
        p=ROOT/entry['directory']/'module.json';m=json.loads(p.read_text())
        m['level']='intermediate' if m['id'] in intermediate_original else 'beginner'
        m.setdefault('tags',[])
        write(p,json.dumps(m,ensure_ascii=False,indent=2))
    entries=[e for e in manifest['modules'] if e['id'] not in new_ids]
    counts={t['id']:sum(json.loads((ROOT/e['directory']/'module.json').read_text())['track']==t['id'] for e in entries) for t in manifest['tracks']}
    last={t['id']:next((e['id'] for e in reversed(entries) if json.loads((ROOT/e['directory']/'module.json').read_text())['track']==t['id']),None) for t in manifest['tracks']}
    for m in NEW:
        track=m['track'];counts[track]+=1;number=counts[track]
        folder=ROOT/TRACK_DIRS[track]/f"{number:02}-{m['id']}"
        version=next(t['version'] for t in manifest['tracks'] if t['id']==track)
        section_texts=[('idea','Understand the idea',m['idea']),('example','Follow a concrete example',m['example']),('trace','Trace the execution',m['walk']),('failure','Break it and reason about the repair',m['failure']+'\n\n**Remember:** '+m['cue'])]
        for sid,title,body in section_texts:write(folder/(sid+'.md'),f'## {title}\n\n{body}')
        exercises=[]
        for eid,title,prompt,answer in [('repair','Diagnose and repair',m['repair'],m['fix']),('transfer','Change the situation',m['transfer'],m['adaptation'])]:
            write(folder/'practice'/f'{eid}.md',f'## {title}\n\n{prompt}\n\nBefore opening a reference, write your prediction, the exact change, how you would verify it, and why it works. Use synthetic data and a separate lab. State clearly which checks you actually ran.')
            write(folder/'answers'/f'{eid}.md',f'## One valid {eid}\n\n{answer}\n\nA different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.')
            exercises.append(dict(id=eid,kind=eid,title=title,minutes=30,file=f'practice/{eid}.md',solutionFile=f'answers/{eid}.md'))
        questions=[];keys={}
        for i,original in enumerate(m['questions']):
            question=dict(original)
            order=list(range(len(question['options'])))
            random.Random(hashlib.sha256((m['id']+str(i)).encode()).hexdigest()).shuffle(order)
            question['options']=[original['options'][j] for j in order]
            question['correctIndex']=order.index(original['correctIndex'])
            key=f'q{i+1}';questions.append({k:v for k,v in {'id':key,**question}.items() if k not in ['correctIndex','explanation']})
            keys[key]={k:question[k] for k in ['correctIndex','explanation']}
        write(folder/'quiz.json',json.dumps(questions,ensure_ascii=False,indent=2));write(folder/'answers/quiz.json',json.dumps(keys,ensure_ascii=False,indent=2))
        diagram='flowchart TD\n'+'\n'.join(f' N{i}["{label}"]' for i,label in enumerate(m['steps']))+'\n'+'\n'.join(f' N{i} --> N{i+1}' for i in range(len(m['steps'])-1))
        recap=diagram+f'\n N{len(m["steps"])-1} --> C{{"What if this fails or repeats?"}}\n C --> R["Check the stated rule and observe the boundary"]\n R -. "try the changed case" .-> N0'
        metadata={k:m[k] for k in ['id','track','title','level','outcome','useCase','benefits','drawbacks','tags','hours']}
        metadata.update(number=number,version=version,book='',cue=m['cue'],prerequisite=m['prerequisite'] or last[track],
          sections=[dict(id=sid,title=title,file=sid+'.md') for sid,title,_ in section_texts],exercises=exercises,
          visuals=[dict(title='The mechanism at a glance',placement='overview',code=diagram),dict(title='Recap: path, failure, and recovery',placement='recap',code=recap)],
          trace=[dict(title=m['steps'][0],detail=m['idea'].split('\n\n')[0]),dict(title='Follow one item',detail=m['walk']),dict(title='Try the failure',detail=m['failure'])],
          sources=[dict(title=title,url=url) for title,url in m['sources']],reading=[],
          recallPrompt='Without notes: '+m['outcome']+' Explain one example and one failure.',lab=m['lab'])
        write(folder/'module.json',json.dumps(metadata,ensure_ascii=False,indent=2))
        write(folder/'README.md',f"# {number}. {m['title']}\n\n**{m['level'].title()} · about 2 hours with practice**\n\n{m['outcome']}\n\n## Use it\n\n{m['useCase']}\n\n**Benefit:** {m['benefits']}\n\n**Cost or limit:** {m['drawbacks']}\n\n## Work in this order\n\n1. [Understand](idea.md).\n2. [Example](example.md).\n3. [Execution trace](trace.md).\n4. [Failure](failure.md).\n5. [Repair practice](practice/repair.md).\n6. [Changed-condition practice](practice/transfer.md).\n\nTake the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.\n\n## Reference\n\n"+'\n'.join(f'- [{title}]({url})' for title,url in m['sources']))
        entries.append(dict(id=m['id'],directory=str(folder.relative_to(ROOT))))
        last[track]=m['id']
    # Cumulative checks cover each tool/service, alongside the final changed-case practice.
    for track, capstone in [('ops','ops-toolkit-capstone'),('cloud','cloud-architecture'),('events','events-replay-capstone')]:
        target=next(e for e in entries if e['id']==capstone);folder=ROOT/target['directory']
        questions=json.loads((folder/'quiz.json').read_text());keys=json.loads((folder/'answers/quiz.json').read_text())
        for entry in entries:
            m=json.loads((ROOT/entry['directory']/'module.json').read_text())
            if m['track']!=track or m['id']==capstone:continue
            source=ROOT/entry['directory'];question=json.loads((source/'quiz.json').read_text())[0]
            answer=json.loads((source/'answers/quiz.json').read_text())[question['id']]
            key='review-'+m['id'];questions.append({**question,'id':key,'prompt':m['title']+': '+question['prompt'],'covers':m['id']});keys[key]=answer
        write(folder/'quiz.json',json.dumps(questions,ensure_ascii=False,indent=2));write(folder/'answers/quiz.json',json.dumps(keys,ensure_ascii=False,indent=2))
    frontend_order=['frontend-browser','frontend-data-contracts','frontend-runtime','frontend-typescript','frontend-state','frontend-vue-components','frontend-vue','frontend-experience','frontend-async-coordination','frontend-web-platform','frontend-vue-reactivity','frontend-vue-composables','frontend-vue-async','frontend-vue-routing-store','frontend-vue-forms','frontend-vue-performance','frontend-vue-testing','frontend-browser-security','frontend-react','frontend-next','frontend-capstone','frontend-delivery-capstone']
    ordered=[]
    for track in manifest['tracks']:
        rows=[(e,json.loads((ROOT/e['directory']/'module.json').read_text())) for e in entries]
        rows=[(e,m) for e,m in rows if m['track']==track['id']]
        if track['id']=='frontend': rows.sort(key=lambda pair: frontend_order.index(pair[0]['id']) if pair[0]['id'] in frontend_order else 99)
        rows.sort(key=lambda pair: 0 if pair[1]['level']=='beginner' else 1)
        previous=None
        for sequence,(entry,m) in enumerate(rows,1):
            m['sequence']=sequence;m['prerequisite']=previous;previous=m['id']
            write(ROOT/entry['directory']/'module.json',json.dumps(m,ensure_ascii=False,indent=2));ordered.append(entry)
    entries=ordered
    manifest['modules']=entries;manifest['contentVersion']='2026-10-21-intermediate'
    for t in manifest['tracks']:
        t['hours']=sum(json.loads((ROOT/e['directory']/'module.json').read_text())['hours'] for e in entries if json.loads((ROOT/e['directory']/'module.json').read_text())['track']==t['id'])
    write(INDEX,json.dumps(manifest,ensure_ascii=False,indent=2))
    for track,directory in TRACK_DIRS.items():
        rows=[(e,json.loads((ROOT/e['directory']/'module.json').read_text())) for e in entries]
        rows=[(e,m) for e,m in rows if m['track']==track]
        text='# '+next(t['title'] for t in manifest['tracks'] if t['id']==track)+'\n\nStart with Beginner. Continue to Intermediate when you can explain and repair the core example. Existing module URLs and progress are preserved.\n'
        for level in ['beginner','intermediate']:
            text+='\n## '+level.title()+'\n\n'
            for e,m in rows:
                if m['level']==level:text+=f"- [{m['title']}]({Path(e['directory']).name}/README.md): {m['outcome']}\n"
        write(ROOT/directory/'README.md',text)
    print('Added',len(NEW),'chapters; total',len(entries))
chapter('frontend','data-contracts','JavaScript values at API boundaries','beginner',
 'Distinguish missing, null, false, zero, and shared nested state when adapting API data.',
 '''A browser receives values, not intentions. A missing field can mean “leave unchanged.” null can mean “clear it.” false and zero can be valid choices. Decide those meanings in the API contract before choosing a default operator.

Use ?? when the fallback should apply to null or undefined. Use || only when all falsey values should trigger the fallback. Destructuring and spread copy one level. A new outer object may still share nested objects with the original. That can make Cancel accidentally change the saved record.

Treat JSON as outside input. JSON.parse proves that text is valid JSON; it does not prove that the result has a ticket ID, an allowed status, or a sensible array shape. Validate at the boundary, then pass a stable internal shape to components.''',
 '''```js
const api = { retries: 0, muted: false, note: null }
const retries = api.retries ?? 3 // preserves 0
const muted = api.muted ?? true // preserves false

const saved = { title: 'Export fails', tags: ['billing'] }
const draft = { ...saved, tags: [...saved.tags] }
draft.tags.push('urgent') // does not change saved.tags
```

For a PATCH request, omit note to leave it alone; send note:null only if the server contract means “clear.” Do not invent that meaning on the client alone.''',
 '''Trace load → validate → adapt → edit draft → submit → accept server result. Keep server data separate from unsaved edits. Test an absent field, explicit null, false, zero, and an empty string. They are five distinct cases.

If a nested structure is complex, copy the fields the form actually edits rather than cloning an entire model graph. structuredClone supports many values but not functions or every host object; it is not a universal serialization protocol.''',
 'Using value || default can silently change a valid zero. Copying only the outer object can leak draft changes. Parsing valid JSON can still produce the wrong type.',
 'An edit form shallow-copies a ticket, pushes to draft.tags, then Cancel leaves the new tag on the saved list. Repair ownership and show a test.',
 'Create a separate editable tags array and update saved state only after a deliberate save result. Test that Cancel preserves the original array contents. Test a failed save too. Copying the outer object alone is insufficient.',
 'The server adds an optional retry limit. How do you preserve an explicit limit of zero?',
 'Validate that supplied values are allowed numbers, then use ?? for absence/null only if the contract treats both as default. Test zero separately. If null means “unlimited,” use an explicit branch rather than ?? to erase that meaning.',
 [q('Which fallback preserves a valid 0?','value || 3','value ?? 3','Boolean(value)',1,'Nullish fallback preserves zero, false, and empty strings.'),q('Does {...record} copy nested arrays?','Yes, recursively','No, it copies their references','Only when frozen',1,'Spread is a shallow copy.'),q('What does JSON.parse validate?','The full business schema','JSON syntax only','Server permissions',1,'Shape and meaning need additional checks.')],
 'Absence is a contract. Copy only what you own.', ['API values','Validate shape','Adapt meanings','Independent edit draft','Accept or cancel'], [('MDN nullish coalescing',MDN+'JavaScript/Reference/Operators/Nullish_coalescing')],usecase='Support forms with optional flags, numeric limits, and editable tag lists.',benefits='Fewer invisible defaulting and Cancel bugs.',drawbacks='Boundary validation and draft ownership require explicit decisions.',tags=['javascript','forms','contracts'])

chapter('frontend','async-coordination','Promises: overlap, cancel, and limit work','intermediate',
 'Choose sequential or parallel work and prevent stale results without losing useful failures.',
 '''await describes a dependency: the next line waits for that promise in this function. Two awaits in sequence may waste time when their inputs are independent. Promise.all waits for all successes but rejects when one rejects; it does not automatically cancel the others. allSettled preserves each outcome when partial results are useful.

Cancellation and acceptance are different. AbortController can stop a supported fetch. A request number or active flag says whether a result may still update this screen. Guard error and loading state as well as rows.

Parallel does not mean unlimited. Launching 10,000 uploads at once can exhaust memory and connections. Use a bounded worker pool or a queue. Retry only a safe operation and only within a deliberate attempt/time limit.''',
 '''```js
const [ticket, members] = await Promise.all([
  readTicket(id), readAllowedMembers(workspaceId)
]) // independent reads; both must succeed for this view

const results = await Promise.allSettled(files.map(validateSmallFile))
const errors = results.filter(r => r.status === 'rejected')
// For large/network work, use a concurrency limit instead of unbounded map.
```

Abort a prior search when starting the next one. Still check which request is current before publishing its result.''',
 '''Draw the dependency graph. Loading a ticket and a member directory can overlap. Loading comments using an ID returned by a creation request cannot begin before that ID exists.

For a stale search: A starts, B starts, B succeeds, A fails. The final UI should show B and no stale error. Use controlled promises to reproduce this exact order. Avoid a fixed sleep as proof.''',
 'Promise.all does not undo a completed write when another promise fails. A spinner hidden in every finally block can be cleared by obsolete work.',
 'A screen fetches three independent panels sequentially and discards all content when one optional panel fails. Improve both latency and partial failure behavior.',
 'Start independent reads together. Use allSettled or separate panel states when partial success is useful. Keep required data failure distinct from optional failure. Show which panel can retry. Do not imply that rejecting a promise cancels or rolls back other requests.',
 'Bulk-upload 500 attachments. What changes from the three-panel case?',
 'Bound concurrency, retain per-file outcomes, support cancellation, and use stable upload identities for retries. Progress should count completed files/bytes deliberately. A single Promise.all over all uploads is not a backpressure strategy.',
 [q('Promise.all rejects. What happens to other requests?','They are automatically cancelled','They may still continue','Their writes roll back',1,'Promise aggregation does not cancel underlying work.'),q('Which operation waits for every settled outcome?','Promise.allSettled','Promise.race','A synchronous forEach',0,'allSettled returns fulfilled/rejected results for each input.'),q('What must a latest-request guard protect?','Rows only','Rows, error and loading state','Only console logs',1,'Every visible state update can become stale.')],
 'Overlap independent work. Bound the amount. Accept only current results.', ['Dependency graph','Start bounded work','Wait or cancel','Accept current outcome','Render useful partial states'], [('MDN Promise',MDN+'JavaScript/Reference/Global_Objects/Promise')],usecase='Dashboards, typeahead, and attachment uploads.',benefits='Less avoidable waiting and fewer stale screens.',drawbacks='Parallel requests need per-operation ownership and limits.',tags=['javascript','async','performance'])

chapter('frontend','typescript','TypeScript: make invalid states harder to express','beginner',
 'Model request states and narrow outside data instead of hiding uncertainty with any.',
 '''TypeScript checks code before it runs. It does not validate JSON at runtime. A cast tells the compiler what you claim; it does not turn a string into a number or verify an API response.

A discriminated union uses one field to distinguish valid shapes. A loading state does not need fake rows and an error at the same time. Narrow the union before reading a field that exists only in one variant.

Use unknown for data you have not checked. Keep interfaces small at the component boundary. Prefer a clear union for status to several booleans that allow impossible combinations such as loading=true and finished=true.''',
 '''```ts
type Ticket = { id: string; title: string }
type LoadState =
  | { kind: 'loading' }
  | { kind: 'ready'; rows: Ticket[] }
  | { kind: 'failed'; message: string }

function heading(state: LoadState) {
  if (state.kind === 'ready') return `${state.rows.length} tickets`
  return state.kind === 'failed' ? state.message : 'Loading tickets'
}
```

Write a parser that accepts unknown and rejects missing/non-string IDs before creating a Ticket. Do not use response.json() as Ticket[] as your validation step.''',
 '''At compile time, narrowing follows kind. At runtime, a parser checks actual values. Once parsed, UI code can work with the smaller trusted shape. Recheck when a new outside boundary is crossed.

For an exhaustive switch, assign the unreachable value to never. A later added state can then produce a compiler error in code that forgot to handle it.''',
 'Non-null assertions hide absence but do not create a DOM element. any spreads unchecked assumptions across the program. Optional properties can conceal a missing required business decision.',
 'A request store has loading, success, failed, rows, and error booleans/fields with contradictory combinations. Replace it with valid shapes.',
 'Use a tagged union with only the fields each state permits. Define transitions for load, success, and failure. Keep old rows deliberately in a separate refreshing variant if the UI supports stale content while loading; do not accidentally invent it with booleans.',
 'The API sometimes returns id:null. Does a TypeScript interface fix it?',
 'No. Validate actual response data and map/reject malformed records according to the contract. Test the parser with null and wrong primitive types. A compile-time cast is not a repair.',
 [q('Does an as Ticket cast validate JSON?','Yes','No','Only in production builds',1,'Casts do not execute validation.'),q('What does state.kind narrow?','The allowed union variant','The network response latency','The database permissions',0,'A discriminator connects a tag to a valid shape.'),q('What should unvalidated input usually start as?','any everywhere','unknown, then checked','never',1,'unknown requires checks before use.')],
 'Types check your claims. Parsers check outside values.', ['Unknown input','Runtime checks','Typed model','Narrowed state','Handled UI branch'], [('TypeScript narrowing','https://www.typescriptlang.org/docs/handbook/2/narrowing.html')],usecase='API adapters and reusable Vue components.',benefits='Missing states and unsafe property reads surface earlier.',drawbacks='Types still need runtime validation at outside boundaries.',tags=['typescript','contracts'])

chapter('frontend','web-platform','HTTP, browser caching, and the real network path','intermediate',
 'Separate HTTP caching, application state, CORS, cookies, and request success.',
 '''fetch resolves for an HTTP 404 or 500. Check response.ok before treating the body as success. A network failure is different from a server returning a deliberate error response.

The browser HTTP cache, a service worker, your query cache, and the server cache are separate copies. Cache-Control describes HTTP caching policy. An ETag can let the server say “not changed.” A fresh fetch call does not prove the server recomputed the data.

Cookies are sent according to origin/site, credentials mode, SameSite, and cookie attributes. CORS is a browser response-access rule, not authorization. A preflight request checks whether the browser may send a certain cross-origin request. Inspect both request and response headers before changing settings.''',
 '''```js
const response = await fetch('/api/tickets', {
  headers: { Accept: 'application/json' }
})
if (!response.ok) throw new Error(`Load failed (${response.status})`)
const data = await response.json()
```

In DevTools, record status, initiator, cache indication, request ID, and Cache-Control. Compare a normal reload and a deliberate cache-disabled debugging run. Disabling cache is a diagnostic, not a production fix.''',
 '''Trace DNS → connection/TLS → request headers → server response → HTTP cache → app adapter → UI state. When the page is stale, identify which layer supplied the stale copy.

A 304 response is used with a cached representation. A 200 with old data can come from a backend cache. A CORS error may hide a response from JavaScript while the server still received the request. Do not assume a browser error means no side effect happened.''',
 'Returning Access-Control-Allow-Origin:* does not make cookie-based cross-origin requests universally work. Sending a retry after a hidden response can repeat a server write.',
 'A save returns 500 but the UI shows success because fetch resolved. Repair the boundary and the visible state.',
 'Check response.ok and parse the expected error format safely. Keep the draft on failure and distinguish unknown write outcome from a confirmed validation rejection. Add a test where fetch resolves with status 500.',
 'A user sees old data after refresh. How do you investigate without blindly adding timestamps to every URL?',
 'Inspect browser cache headers, service worker interception, app query state, and server cache behavior. Follow the request ID to the response source. Choose a freshness policy and invalidation at the responsible layer rather than disabling every cache.',
 [q('fetch receives HTTP 500. Does it normally reject solely for that status?','Yes','No','Only with JSON',1,'HTTP errors need an explicit status check.'),q('CORS primarily controls what?','Server-side ownership','Browser cross-origin response access','SQL isolation',1,'It is not a substitute for authentication and authorization.'),q('A new fetch call proves backend data was recomputed?','Yes','No','Only with GET',1,'Caches can serve the response at several layers.')],
 'Name the layer before changing the setting.', ['Browser request','HTTP status and headers','Cache layer','Validated data','Visible result'], [('MDN HTTP caching',MDN+'HTTP/Guides/Caching'),('MDN Fetch',MDN+'API/Fetch_API/Using_Fetch')],usecase='Stale dashboards and cross-origin application debugging.',benefits='Finds the actual boundary instead of adding random cache flags.',drawbacks='Several caches and identity rules can interact.',tags=['http','browser','debugging'])

chapter('frontend','vue-reactivity','Vue 3: refs, proxies, computed, and timing','intermediate',
 'Follow a tracked read and explain why nextTick differs from ordinary assignment.',
 '''reactive returns a proxy. Vue can track property reads through that proxy and notify effects when relevant writes happen. ref creates a reactive value wrapper. JavaScript uses .value; templates unwrap refs in supported contexts.

computed should calculate a value from tracked sources. Keep it free of network calls and mutations of unrelated state. watch is for a deliberate side effect. A destructured primitive is no longer a proxy property access; use toRef/toRefs or a getter when a live connection is required.

State assignment happens synchronously, but DOM updates are batched. nextTick waits for Vue’s pending DOM update flush. It does not wait for a network request, image decoding, or every future render. Measure an element after the relevant update, not by guessing a timeout.''',
 '''```ts
import { ref, computed, nextTick } from 'vue'
const query = ref('')
const tickets = ref([{ title: 'Refund request' }])
const visible = computed(() => tickets.value.filter(t =>
  t.title.toLowerCase().includes(query.value.toLowerCase())))

async function openPanel() {
  panelOpen.value = true // panelOpen is a ref owned by this component
  await nextTick()
  panelElement.value?.focus() // template ref, after its v-if DOM update
}
```''',
 '''Read query inside computed → Vue records that dependency. Change query → computed becomes stale → a dependent render asks for the new value. Several synchronous writes can lead to one DOM update batch.

Use shallowRef when you intentionally treat a large outside object as one replaceable value. Deep mutation will not behave like an ordinary deep reactive ref. Choose it for a reason, such as an external editor instance, not as a universal speed switch.''',
 'Watching a computed merely to copy it into another ref creates two sources. Mutating a raw object behind a proxy can bypass the access path you expected Vue to track.',
 'A modal’s input ref is null immediately after setting open=true under v-if. Repair focus timing.',
 'Set the state, await nextTick, then focus the template ref if it exists. Handle closing/unmounting during the wait. Do not replace the timing contract with setTimeout(100). Test focus when opened by keyboard.',
 'A large third-party editor object causes expensive reactive wrapping. What would you consider?',
 'Keep the external instance outside deep reactivity or use shallowRef/markRaw deliberately. Replace the reactive reference when the UI must notice a new instance. Document which internal changes are not tracked and clean up the instance on unmount.',
 [q('What does nextTick wait for?','All pending HTTP requests','Vue’s pending DOM update flush','The next user click',1,'It is a DOM update timing tool, not a general async barrier.'),q('A computed getter should normally do what?','Send an email','Derive a value from sources','Mutate its own input',1,'Pure derivation keeps dependencies predictable.'),q('Destructuring a reactive numeric property gives what?','A primitive current value','A new live ref automatically','A database cursor',0,'Use a linked ref/getter for ongoing tracking.')],
 'Track the read. Batch the DOM. Wait for the right boundary.', ['Reactive source','Tracked getter','Invalidation','Batched DOM patch','nextTick focus or measure'], [('Vue reactivity',VUE+'reactivity-fundamentals.html'),('Computed values',VUE+'computed.html')],usecase='Complex editable Vue screens and modal focus.',benefits='Predictable derivation and fewer timing guesses.',drawbacks='Deep and shallow tracking have different contracts.',tags=['vue3','reactivity'])

chapter('frontend','vue-components','Vue components: props, events, slots, and v-model','beginner',
 'Design a reusable component API with one owner and explicit update events.',
 '''A component API is a small agreement. Props bring information in. Events ask the owner to change something. Slots let a caller supply presentation while the component owns behavior. Decide which part owns the saved value, draft, and focus.

Avoid mutating a nested object received as a prop. A shallow readonly prop boundary does not make every nested value immutable. Emit an update or edit an independent draft instead.

v-model is a prop/event convention. In Vue 3.4+, defineModel is a convenience macro. The older explicit modelValue plus update:modelValue contract is still useful to understand. Give events meaningful types and keep accidental HTML attributes from landing on the wrong element in wrapper components.''',
 '''```vue
<script setup lang="ts">
defineProps<{ modelValue: string; disabled?: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
<template>
  <label>Ticket title
    <input :value="modelValue" :disabled="disabled"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)">
  </label>
</template>
```

The parent can use v-model="draft.title". Add an error slot only when callers need to customize that content; do not expose every internal DOM node as an API.''',
 '''Parent changes modelValue → child renders it. User types → child emits a value → parent accepts it → new prop flows down. This loop makes ownership visible.

For a wrapper, inspect whether id, aria-describedby, and class reach the actual input or only the wrapper div. Accessible names and error associations are part of the component’s contract.''',
 'A component that both owns a private value and blindly watches the parent prop can overwrite an in-progress edit. A custom input without a real label is harder to use even when v-model works.',
 'A reusable editor directly changes props.ticket.title and Cancel cannot undo it. Design a clearer API.',
 'Use an owned parent draft and emit title updates, or create a local draft with explicit Save/Cancel events. Define when an external record change resets that draft. Test Cancel, parent replacement, and a failed save.',
 'The same component is used inside a labelled form field. How should it forward accessibility attributes?',
 'Make the actual input receive the ID and described-by attributes, and define label responsibility clearly. Use inheritAttrs:false and explicit forwarding when the default fallthrough is wrong. Test the accessible name and error relation.',
 [q('What does an update event do?','Requests the owner to change state','Mutates the parent automatically in every case','Commits to the database',0,'The owner decides how the emitted value updates its state.'),q('Are nested objects in props deeply immutable?','Always','No','Only in TypeScript',1,'Avoid mutating shared nested values through props.'),q('What is a slot useful for?','Caller-supplied presentation within a behavior boundary','Server authorization','Replacing all state ownership',0,'Slots compose UI without requiring the child to know every caller layout.')],
 'Props describe. Events request. Slots compose.', ['Owner value','Prop flows down','User input','Typed event','Owner accepts new value'], [('Vue component v-model','https://vuejs.org/guide/components/v-model.html'),('Fallthrough attributes','https://vuejs.org/guide/components/attrs.html')],usecase='Reusable form controls and ticket editors.',benefits='Small component contracts and testable ownership.',drawbacks='A very configurable component can become harder than two focused components.',tags=['vue3','components','accessibility'])

chapter('frontend','vue-composables','Composables: reusable behavior without hidden global state','intermediate',
 'Extract reactive behavior with explicit inputs, lifecycle cleanup, and a predictable return API.',
 '''A composable is a function that packages reusable stateful logic. It is not simply any helper with use in its name. A pure formatter is often just a function.

Choose where state is created. A ref inside useSelection gives each call its own selection. A ref at module scope is shared by every caller in that JavaScript runtime. That can be deliberate for a store, but dangerous for per-request state in server rendering.

Return refs when callers need to destructure reactive values. Accept a getter/ref when the input should remain live, and watch that input explicitly. Register lifecycle cleanup while the component context is available. Detached listeners, intervals, and subscriptions must have a lifetime owner.''',
 '''```ts
import { ref, onUnmounted } from 'vue'
export function useSelection() {
  const selectedId = ref<string | null>(null) // per call
  const select = (id: string) => { selectedId.value = id }
  const clear = () => { selectedId.value = null }
  return { selectedId, select, clear }
}

export function useWindowResize(update: () => void) {
  window.addEventListener('resize', update)
  onUnmounted(() => window.removeEventListener('resize', update))
}
// Browser-only example: guard window access in SSR code.
```''',
 '''Two components call useSelection. Each call allocates one ref, so they can select different tickets. Move the ref above the function and both callers now share it. Neither version is automatically better; the intended ownership decides.

Test composables with pure seams when possible. For lifecycle-dependent behavior, mount a small component and verify listeners are removed when it unmounts.''',
 'Creating a timer without clearing it can keep updating a vanished view. A composable that silently reads route, store, and global user state is harder to reuse than one with explicit dependencies.',
 'Every ticket pane unexpectedly shares the same selected ID because the ref lives at module scope. Repair or document the ownership.',
 'Move the ref into the composable for independent panes. If shared selection is intended, expose it through a named store and test that shared behavior. Avoid relying on an accidental module singleton.',
 'The composable must work in an SSR application. What browser assumptions must you revisit?',
 'Do not read window or document at module evaluation on the server. Attach browser effects in the appropriate client lifecycle and clean them up. Avoid cross-request singleton state for private user data. Test two independent server requests or isolate per-app state.',
 [q('A ref declared inside each composable call is usually what?','Per call','Always global','A prop',0,'Each invocation creates independent state unless it imports shared state.'),q('Why return refs?','To preserve reactive links when destructured','To encrypt the values','To prevent all writes',0,'Plain primitive returns would be snapshots.'),q('What owns a subscription lifetime?','A deliberate component/store scope','The file name only','The browser forever',0,'Cleanup must match the scope that created the effect.')],
 'Inputs visible. State owned. Effects cleaned up.', ['Explicit input','Owned refs','Reusable behavior','Returned reactive API','Scope cleanup'], [('Vue composables','https://vuejs.org/guide/reusability/composables.html')],usecase='Selection, pagination, subscriptions, and reusable editor behavior.',benefits='Reuse behavior without giant components.',drawbacks='Hidden singleton state and implicit dependencies can make bugs travel.',tags=['vue3','composables','architecture'])

chapter('frontend','vue-async','Vue watchers and async search without stale state','intermediate',
 'Implement a watched request with cleanup, current-result guards, and honest loading/error states.',
 '''Use watch when you want a side effect tied to a specific source. watchEffect tracks reactive reads made during its synchronous execution; reads after the first await do not automatically become dependencies of that effect.

Register cancellation before awaiting. Vue 3.5 onWatcherCleanup must be called synchronously. The watch callback’s onCleanup argument is a useful alternative. Cleanup means the old request no longer owns this view, even if the network cannot be cancelled immediately.

Keep state transitions explicit. A stale response must not publish rows, an error, or loading=false. Decide whether an empty query clears results. Debouncing reduces request frequency but does not establish response order.''',
 '''```ts
watch(query, async (text, _old, onCleanup) => {
  let active = true
  const controller = new AbortController()
  onCleanup(() => { active = false; controller.abort() })
  loading.value = true; error.value = ''
  try {
    const r = await fetch('/api/tickets?q=' + encodeURIComponent(text),
      { signal: controller.signal })
    if (!r.ok) throw new Error('Search failed')
    const body = await r.json()
    if (active) rows.value = body // validate body at the real boundary
  } catch (e) {
    if (active && !controller.signal.aborted) error.value = 'Could not search'
  } finally {
    if (active) loading.value = false
  }
})
```''',
 '''Query A starts and owns active=true. Query B invalidates A: cleanup sets A inactive and aborts it. B becomes the owner. If A finishes later, its active check prevents every visible update.

Test success-success in reverse order, stale failure after success, abort, and unmount. Give each request a controlled deferred response so the test chooses the timeline.''',
 'Putting onWatcherCleanup after await can miss the synchronous registration requirement. Debouncing alone still allows two requests to overlap.',
 'A watcher catches AbortError and shows a red error whenever the user types another character. Repair the error policy.',
 'Treat deliberate cancellation as obsolete work rather than a user-visible failure. Track active ownership, guard state updates, and show real current-request errors. Test changing input while a request is pending.',
 'A route query change and an input edit both trigger search. How do you avoid two unrelated owners?',
 'Choose one search source, often the URL query, and let the input update it deliberately. Watch that source once. Define debounce/navigation behavior and test back/forward. Do not maintain two unsynchronized query strings.',
 [q('Does debounce guarantee response order?','Yes','No','Only with GET',1,'Request start timing does not determine completion order.'),q('Where should onWatcherCleanup be registered?','Synchronously before awaiting','Only after response.json','After unmount',0,'Vue 3.5 requires synchronous registration.'),q('watchEffect automatically tracks a source first read after await?','Yes','No','Only in production',1,'Its automatic tracking covers synchronous reads.')],
 'Cleanup revokes ownership, not just network work.', ['Reactive query','Register cleanup','Fetch current input','Guard every update','Clean next run or unmount'], [('Vue watchers',VUE+'watchers.html')],usecase='Live ticket search and dependent selects.',benefits='Predictable async state under fast input.',drawbacks='Cancellation, ownership, and validation need separate handling.',tags=['vue3','async','testing'])

chapter('frontend','vue-routing-store','Vue Router and Pinia: choose where state lives','intermediate',
 'Use URL state, component state, and stores deliberately, including route changes and server rendering.',
 '''A route is part of the user’s working context. Search, selected workspace, and page often need to survive refresh or be shared. Put those values in a stable URL contract and parse them, including invalid inputs.

A store is useful for shared application state and named actions. It does not automatically solve server cache freshness. Keep remote data, local drafts, and permissions separate. With Pinia, storeToRefs preserves reactivity when destructuring state/getters; actions can be called from the store normally.

Route components can be reused when params change. Watching only onMounted can leave the old ticket on screen after navigation. Watch the relevant ID or use a deliberate route data-loading strategy. A navigation guard improves UX but the server must still enforce access.''',
 '''```ts
const route = useRoute()
const ticketId = computed(() => String(route.params.id))
watch(ticketId, loadTicket, { immediate: true }) // loadTicket guards stale work

const workspace = useWorkspaceStore()
const { selectedWorkspaceId } = storeToRefs(workspace)
// Route update: router.replace({ query: { ...route.query, q: text } })
```

These fragments assume Vue Router and Pinia are installed and imported. Parse numeric pages into bounded positive integers rather than blindly using Number(query.page).''',
 '''Direct URL → parse query/params → establish workspace context → load allowed server data → render → user changes filter → update URL. Back navigation should restore meaningful state.

For an unsaved form, define whether navigation prompts, saves a draft, or discards it. Browser Back and an in-app link should follow the same user-facing policy.''',
 'A single global editing object can make two open panes overwrite each other. A route guard is not server authorization. Query-string arrays and absent values require parsing.',
 'Navigating from /tickets/1 to /tickets/2 keeps the old data because loading only happens onMounted. Repair it.',
 'React to the relevant route ID and cancel/ignore obsolete loads. Reset or preserve the edit draft according to an explicit rule. Test param navigation without full component remount and back navigation.',
 'Two workspaces use the same ticket number. What must a client cache key include?',
 'Include the relevant workspace/tenant identity and any query dimensions that change the answer. Invalidate/reload on identity changes. Never treat a cache key as permission; check access on the server.',
 [q('Can a route component be reused for another ID?','Yes','No','Only without params',0,'Do not assume onMounted runs again for every param update.'),q('What preserves Pinia state reactivity when destructuring?','storeToRefs','JSON.stringify','A shallow primitive assignment',0,'storeToRefs returns reactive references to state/getters.'),q('Does a client route guard authorize a database write?','Yes','No','Only with Pinia',1,'Server-side access checks remain necessary.')],
 'URL for context. Store for sharing. Server for authority.', ['URL context','Parsed route','Scoped store state','Allowed data load','Back and forward behavior'], [('Vue Router data fetching','https://router.vuejs.org/guide/advanced/data-fetching.html'),('Pinia core concepts','https://pinia.vuejs.org/core-concepts/')],usecase='Multi-workspace support dashboards.',benefits='Shareable context and predictable navigation.',drawbacks='Stores can become dumping grounds without ownership rules.',tags=['vue3','routing','pinia'])

chapter('frontend','vue-forms','Forms that survive real editing','intermediate',
 'Handle validation, dirty state, unsaved changes, and server conflicts without losing user work.',
 '''A form is a small state machine: pristine, editing, validating, saving, saved, or failed. Some checks are immediate, such as a required title. Others depend on the server. Avoid showing aggressive errors before a user has had a reasonable chance to enter a value.

Keep the draft when a request fails. A successful response may contain normalized data or a new version; accept that deliberately. If the record changed elsewhere, do not silently overwrite it. Use a version/ETag contract where the server supports it.

An error must say what can be fixed. Connect it to the field, keep the label visible, and focus a useful location after a failed submission. Disabling a button is not an explanation of why saving is blocked.''',
 '''```ts
const draft = reactive({ title: '', priority: 'normal' })
const saving = ref(false)
const errors = ref<Record<string, string>>({})
async function save() {
  if (saving.value) return
  errors.value = draft.title.trim() ? {} : { title: 'Enter a title' }
  if (Object.keys(errors.value).length) return
  saving.value = true
  try { await submitDraft({ ...draft }) }
  catch { errors.value = { form: 'Could not save. Your edits are kept.' } }
  finally { saving.value = false }
}
```

submitDraft must check HTTP status and map field/conflict errors; this fragment shows ownership, not a complete request adapter.''',
 '''Type → dirty draft → client checks → request with expected version → server validation/authorization → success or conflict → keep or reconcile draft. An old successful response must not overwrite newer edits typed during the request.

Test paste, keyboard submit, double-click, slow save, field rejection, network loss, and record replacement. Use a visible saving status and a clear retry path.''',
 'Resetting from props on every server refresh can wipe a dirty draft. Sending the whole entity can include server-owned fields. A stale response can erase a newer edit.',
 'A background refresh replaces the record prop and a watcher resets an unsaved description. Repair the reset policy.',
 'Separate saved snapshot and draft. Reset only on explicit record change when safe, successful save acceptance, or user-confirmed discard. Detect a dirty draft before applying a refresh. Test refresh during editing.',
 'Two agents edit the same ticket. What would a version-aware save look like?',
 'Send an expected version or If-Match under a documented API. The server rejects stale writes. Show the conflict and offer compare/reload/merge while keeping the local draft. A client version counter alone cannot enforce database concurrency.',
 [q('What should a network failure usually preserve?','The user’s draft','Only the spinner','No local state',0,'Data entry is work; failure should not erase it.'),q('What prevents a stale overwrite at the authority boundary?','A server-enforced version check','A longer debounce','Only a hidden Save button',0,'The server must enforce the concurrency contract.'),q('Should every prop refresh reset a dirty draft?','Always','Only under an explicit safe reset rule','Only if it is JSON',1,'Unconditional synchronization loses edits.')],
 'A failed save should lose the request, not the work.', ['Owned draft','Accessible checks','Versioned request','Server result','Preserve or reconcile'], [('Vue forms',VUE+'forms.html'),('WAI form validation','https://www.w3.org/WAI/tutorials/forms/validation/')],usecase='Support-ticket editing with concurrent agents.',benefits='Fewer lost edits and more understandable failures.',drawbacks='Dirty-state and conflict handling require product decisions.',tags=['vue3','forms','ux'])

chapter('frontend','vue-performance','Vue performance: measure the expensive boundary','intermediate',
 'Find whether a slow interaction comes from work, rendering, layout, or network delay.',
 '''Start with a measured symptom: typing takes 200 ms to appear with 5,000 tickets. Profile before choosing a fix. Filtering, component updates, layout, and network work have different repairs.

Stable props can reduce avoidable child updates. Stable keys preserve identity. Code splitting reduces initial work for features the user has not opened. List virtualization reduces mounted rows, but it must preserve focus, keyboard navigation, and scroll expectations.

Do not memoize a correctness bug. A wrong state owner or stale response remains wrong when cached. shallowRef, v-memo, and custom optimizations add contracts that future maintainers must understand. Use them after identifying a meaningful cost.''',
 '''```ts
const visible = computed(() => tickets.value.filter(matchesFilter))
// Instead of passing selectedId to every row and asking each to compare:
// <TicketRow :ticket="ticket" :active="ticket.id === selectedId" />
// Only rows whose active value changes need that prop change.
```

For a heavy optional editor: const Editor = defineAsyncComponent(() => import('./Editor.vue')). Measure initial transfer/parse time and the first editor-open wait separately.''',
 '''Record interaction → long task → flame chart → expensive function or layout. Change one thing and compare with the same synthetic dataset/device conditions. Keep a correctness check alongside the timing check.

If the server sends 50,000 rows, frontend tricks may hide a poor data boundary. Consider server filtering, pagination, and bounded responses before rendering every row.''',
 'A fast desktop can hide mobile main-thread cost. Virtualization can break screen-reader context. A deep watcher over a large tree may run more work than the user action needs.',
 'A developer adds memoization everywhere but the slow step is a synchronous sort of 50,000 rows on each keypress. Propose a measured repair.',
 'Bound/filter data deliberately, avoid repeated full sorting when inputs have not changed, and consider moving expensive computation off the input path. Measure before/after. Verify stale response handling and keyboard interaction remain correct.',
 'Virtualizing rows makes the focused input disappear while scrolling. What must the design address?',
 'Keep edit/focus state outside transient row instances or retain the active row deliberately. Provide keyboard navigation semantics and test assistive technology behavior. Performance gains do not justify losing the current user task.',
 [q('What comes before selecting a performance trick?','A repeatable measured symptom','Adding v-memo everywhere','Changing every ref to shallowRef',0,'Find the expensive boundary first.'),q('What do stable keys primarily protect?','Component identity','Network bandwidth automatically','Database indexes',0,'Keys let the framework match items across updates.'),q('Virtualization removes which responsibility?','None of the access/focus responsibilities','All keyboard testing','Server permissions',0,'It reduces DOM work but adds interaction constraints.')],
 'Measure one delay. Fix one cause. Retest the task.', ['Slow interaction','Profile the boundary','Choose one repair','Measure again','Check access and correctness'], [('Vue performance','https://vuejs.org/guide/best-practices/performance.html')],usecase='Large ticket tables and optional rich editors.',benefits='Improves the delay users actually experience.',drawbacks='Optimizations can add stale-state, focus, and maintenance costs.',tags=['vue3','performance'])

chapter('frontend','vue-testing','Vue tests: behavior, timing, and contracts','intermediate',
 'Write component tests for failed saves, async races, and accessible interaction.',
 '''A pure test checks a transformation. A component test mounts a small UI and exercises its public behavior. A browser test verifies real navigation, layout, and browser APIs. Choose the layer that can observe the defect.

Prefer accessible roles and labels when finding controls. A test that clicks .blue-button can pass while the button has no useful name. Wait for Vue updates and promises deliberately. nextTick flushes Vue updates; flushPromises helps pending promise callbacks in tests. Neither proves a real remote service works.

Control time and request outcomes. Resolve B before A to test a race. Return an HTTP rejection to test draft preservation. Keep a few real integration checks so mocks do not invent an API contract that the server does not provide.''',
 '''```ts
// Vue Test Utils / Vitest sketch; imports and the component are project setup.
const wrapper = mount(TicketForm, { props: { initialTitle: 'Old' } })
await wrapper.get('input').setValue('New')
await wrapper.get('form').trigger('submit')
await flushPromises()
expect(wrapper.get('input').element.value).toBe('New')
expect(wrapper.text()).toContain('Your edits are kept')
```

Configure the fake request to reject before asserting this case. Assert the contract and user-visible result rather than every internal ref name.''',
 '''Arrange the state and fake boundary → act as a user → flush the required update boundary → assert visible outcome and emitted contract. Confirm the test fails when the repair is removed.

For focus trapping, hydration, scroll, and browser back behavior, run a real browser check. A simulated DOM does not implement all browser layout/accessibility behavior.''',
 'Testing private implementation details makes refactors expensive. Broad snapshots may miss the important failure. Arbitrary sleeps make the test depend on machine speed.',
 'A component test passes because the fake fetch returns {ok:true} for every input, including unauthorized writes. What is missing?',
 'Test the failed/denied response and verify no success state is shown. Add a server boundary test for permissions. The client fake must model the documented error shape, but cannot prove server authorization itself.',
 'A race only happens after navigating to another ticket. How do you cover it?',
 'Mount with a route or reactive-ID seam, start the first request, change the ID, resolve the new request before the old, and assert only the new ticket remains. Add a browser navigation smoke test for the connected route behavior.',
 [q('What makes a regression test convincing?','It fails before the repair and passes after','It is very long','It checks private variable names',0,'The test must discriminate the broken behavior.'),q('Does nextTick wait for every fetch?','Yes','No','Only with a component test',1,'It waits for Vue’s pending DOM update flush.'),q('Where should real focus/navigation behavior also be checked?','A real browser','Only a pure function test','Only a JSON snapshot',0,'Browser behavior extends beyond a simulated DOM.')],
 'Test the promise the user sees.', ['Arrange a boundary','User action','Controlled async outcome','Visible assertion','Regression and browser check'], [('Vue testing','https://vuejs.org/guide/scaling-up/testing.html'),('Vue Test Utils async','https://test-utils.vuejs.org/guide/advanced/async-suspense.html')],usecase='Changes to complex forms and route-driven panes.',benefits='Repeatable evidence for failure paths.',drawbacks='Mocks and simulated DOM tests have limits.',tags=['vue3','testing'])

chapter('frontend','browser-security','Frontend security that affects everyday code','intermediate',
 'Separate trusted markup, outside text, browser storage, and server authorization.',
 '''Outside text is data. Rendering it as HTML can turn it into executable behavior. Vue’s ordinary interpolation escapes text; v-html crosses a different boundary. If rich HTML is required, use a maintained sanitizer with an explicit policy and keep it updated.

Browser storage is available to code running in the origin. It is not a secret vault. A script injection can read accessible tokens and drafts. Cookie settings, CSRF protection, Content Security Policy, and server access checks address different risks.

Never send a field to the browser just because it is hidden visually. Client props, network payloads, source maps, logs, and analytics can all reveal information. Select permitted data on the server and keep telemetry deliberately small.''',
 '''```vue
<template>
  <p>{{ ticket.title }}</p> <!-- outside text stays text -->
  <!-- v-html="ticket.title" would interpret markup instead. -->
</template>
```

Use textContent for plain DOM text. For external links opened in a new tab, choose safe URL schemes and use rel="noopener noreferrer" where appropriate. A sanitizer for HTML does not automatically validate every business URL policy.''',
 '''Input arrives → validate shape → decide text versus rich content → render through the right boundary → enforce server permissions for actions. Audit the payload and telemetry, not just pixels.

Test a title containing markup-looking text. It should appear as text. Test a direct unauthorized request without using the UI. These are different checks.''',
 'A hidden field in a client payload is still present. A client filter is not a tenant boundary. Escaping output does not validate a destination URL or authorize a mutation.',
 'A tooltip uses v-html for a ticket title returned by users. Repair it without losing ordinary formatting requirements.',
 'Render the title as escaped text. If separate rich content is truly needed, define an allowed format and sanitize it at the render boundary. Test unsafe markup and legitimate content. Keep the title contract plain text if possible.',
 'Analytics records every form field to help debugging. What should change?',
 'Use a minimal event schema that excludes free text, secrets, and sensitive values. Record allowed action names, outcome categories, and non-sensitive identifiers only when needed. Review SDK automatic capture settings and retention/access policies.',
 [q('What does v-html change?','Text is interpreted as HTML','Server authorization is added','JSON gets validated',0,'It crosses a markup interpretation boundary.'),q('Is a hidden client prop secret?','Yes','No','Only on mobile',1,'The browser received it even if it was not displayed.'),q('Does sanitizing HTML establish row access?','Yes','No','Only with CSP',1,'Authorization remains a server responsibility.')],
 'If the browser receives it, the user can inspect it.', ['Outside data','Text or rich-content contract','Safe rendering','Minimal telemetry','Authorized server action'], [('Vue security','https://vuejs.org/guide/best-practices/security.html'),('MDN CSP',MDN+'HTTP/Guides/CSP')],usecase='Rich tooltips, support descriptions, and product analytics.',benefits='Makes common trust boundaries visible in everyday UI work.',drawbacks='Rich content and third-party SDKs require ongoing policy maintenance.',tags=['security','vue3','privacy'])

chapter('frontend','delivery-capstone','Ship a Vue 3 support workspace','intermediate',
 'Connect URL state, reusable components, async data, editing, tests, and measured UX in one small feature.',
 '''Build one vertical feature rather than a gallery of disconnected examples. A support workspace should open directly from a URL, load an allowed ticket list, filter it, open a ticket, edit its title, and preserve edits after a failed save.

Use a small boundary map: router owns context, an API adapter validates responses, a composable owns request lifetime, components render accessible states, and the server owns permission and concurrency rules. Add a store only for state that really crosses component ownership boundaries.

Completion is a demonstration: a happy path, a denied request, a failed save, a reverse-order request race, a keyboard path, and a large-data profile. Explain which evidence came from pure tests, component tests, and a browser.''',
 '''```text
src/api/tickets.ts         HTTP + parsing + error contract
src/composables/useSearch.ts  current request + cleanup
src/stores/workspace.ts    shared workspace identity, if needed
src/components/TicketForm.vue  owned draft + accessible errors
src/views/TicketsView.vue  URL context + composition
src/router/index.ts       routes + navigation UX
```

Write a five-line contract for each file before implementation. Test the observable behavior, not this exact directory spelling.''',
 '''Follow a search from URL to accepted rows. Follow an edit from input to versioned request to reconciled response. Follow a failed save back to a preserved draft. Finally trace an old request that arrives after navigation and prove it has no ownership.

Add one production-style change: a new optional status from the server. Decide how older clients render it. A strict parser can reject unexpected data; a tolerant adapter can preserve unknown states. Choose deliberately.''',
 'A feature can pass isolated tests while its router, API, and component contracts disagree. A polished happy path can still lose drafts or hide denied writes.',
 'The feature looks correct but refresh drops the filter, an old request replaces rows, and a save failure clears the draft. Produce a boundary-based repair plan.',
 'Move shareable filter context into a parsed URL, establish one accepted request owner, and separate the saved record from the editable draft. Add one regression for each defect, then a browser smoke path that connects them. Change one boundary at a time.',
 'A teammate must maintain the feature next month. What short handoff makes your reasoning reusable?',
 'Provide the state ownership map, API/error contract, failure timelines, test commands, and one known limitation. Show how to trace a request ID and reproduce the race. A list of libraries is not an architecture explanation.',
 [q('What should the capstone prove?','Connected behavior across boundaries','Only the number of components','That all state is global',0,'A vertical feature shows how the pieces work together.'),q('Where should shareable filters usually live?','A parsed URL contract','Only a private ref','Only a console log',0,'Users expect refresh, links, and history to preserve context.'),q('What is a useful handoff artifact?','State ownership and failure/test map','A screenshot without behavior','A dependency list only',0,'It explains how to investigate and change the feature.')],
 'One feature. Several boundaries. Observable promises.', ['URL and user intent','API and request owner','Accessible components','Versioned save','Tests and measured experience'], [('Vue scaling up','https://vuejs.org/guide/scaling-up/state-management.html')],usecase='A maintainable multi-pane ticket workspace.',benefits='Turns separate concepts into a feature you can explain and change.',drawbacks='The capstone requires hands-on work beyond reading.',tags=['vue3','capstone','architecture'])
chapter('ux','task-model','Start with the user’s task, not the screen','beginner',
 'Turn a vague feature request into a task, context, success condition, and recovery path.',
 '''A screen is a means to finish a task. “Add a dashboard” is not yet a task. “Find the oldest urgent ticket and assign it before the shift ends” is. Name the user, their goal, what they already know, and what interrupts them.

Separate the user’s mental model from your database model. An agent thinks in tickets, queues, and follow-ups. They may not think in foreign keys or internal service names. Labels should help them predict what an action does.

A journey includes entry, action, feedback, completion, and recovery. It also includes returning later. Ask what context survives a refresh and what happens if the user is interrupted midway. A good design reduces the amount they must remember between those steps.''',
 '''```text
Request: “Add bulk actions.”
Task: A shift lead assigns 15 overdue tickets to the next team.
Known: current queue and team membership.
Risk: selecting the wrong tickets or losing selection after a filter change.
Success: correct tickets assigned, failures visible, undo/recovery clear.
```

Sketch the path with boxes before choosing colors. Show what selected means when pagination or filtering changes.''',
 '''Observe one realistic attempt. Where does the person start? How do they identify the right records? What tells them the action finished? What do they do when only 12 of 15 changes succeed?

Write a decision log: observed problem → design choice → expected benefit → check. This keeps a critique from becoming a contest of taste.''',
 'Copying a competitor’s layout without the same user/context can add irrelevant controls. Showing a database term can make users guess. A success toast can hide partial failure.',
 'A bulk action says “Done” even when three records failed. Redesign the outcome and recovery.',
 'Show a clear result count, identify failed items and reasons that can be acted on, preserve relevant selection, and offer a safe retry for failed items only. Explain whether retry can repeat successful effects. Test with a realistic partial-success task.',
 'The same task is done by a new agent and a power user. How can one flow support both?',
 'Keep the main path understandable with familiar labels and visible state. Add discoverable shortcuts or saved views for frequent work without hiding the basic path. Test both first-use understanding and repeated-task efficiency.',
 [q('Which is the clearest task statement?','Build a modern dashboard','Assign the oldest urgent ticket before handoff','Use a new component library',1,'A task names a user outcome in context.'),q('What should partial success communicate?','Which actions succeeded and how to recover failures','Only a green toast','Only a raw exception',0,'Users need an accurate state and next action.'),q('What makes a design critique useful?','A problem and evidence tied to a task','Personal preference alone','The newest visual trend',0,'Task evidence gives a decision a purpose.')],
 'Who is trying to do what, under which pressure?', ['User and context','Task and known facts','Action path','Visible outcome','Recovery and return'], [('Human-centred design overview','https://www.usability.gov/how-to-and-tools/methods/user-centered-design.html'),('Nielsen usability heuristics','https://www.nngroup.com/articles/ten-usability-heuristics/')],usecase='Feature scoping and UX review for operational workflows.',benefits='Connects interface decisions to outcomes people need.',drawbacks='A task hypothesis still needs observation; a tidy diagram is not user evidence.',tags=['ux','fundamentals'])

chapter('ux','hierarchy','Perception, grouping, and information hierarchy','beginner',
 'Use proximity, similarity, alignment, and contrast to make the page’s structure understandable.',
 '''People scan before they read closely. Visual grouping suggests relationships. Nearby controls look related. Similar styling suggests similar purpose. A border around a group can imply a shared context. These are useful perceptual tendencies, not rules that override every task.

Give the page a primary question. A ticket page might answer “What needs attention now?” Use headings and spacing to distinguish queue context, the main record, and secondary details. If every element is bright and bold, none has priority.

Visual order and keyboard/reading order should agree. CSS can move a button visually while leaving its document position confusing. Use semantic headings and a sensible source order. Do not make color the only signal for priority or failure.''',
 '''```css
.ticket-actions { display: flex; gap: .75rem; flex-wrap: wrap; }
.field-group { margin-block: 1.5rem; }
.field-group > label { display: block; margin-bottom: .4rem; }
```

Before: five equal panels compete with the ticket title. After: one clear record heading, grouped actions beside their record, and secondary metadata under a quieter heading. Explain which task each grouping supports.''',
 '''Ask a person to point to the current queue, the selected ticket, the primary next action, and unsaved state. Do they infer the intended relationships without a tutorial?

Then remove color from the sketch and test reading order by keyboard. Grouping should still be understandable. A decorative divider is not a replacement for a meaningful heading.''',
 'Large gaps inside a field and small gaps between unrelated fields can imply the wrong grouping. A floating global action can look as if it applies only to the nearest item.',
 'A Delete action visually sits between two ticket cards. Users cannot tell which record it affects. Repair the relationship.',
 'Place the action inside a clearly labelled record context and name its target when needed. Use spacing and grouping consistently. For destructive actions, also provide an understandable consequence and recovery policy. Test identification before asking users to click.',
 'The desktop two-column layout becomes one column on mobile. What must remain clear?',
 'Preserve semantic grouping and source order. Keep the primary task and its state together. Test narrow widths, zoom, long labels, and keyboard focus. A responsive grid change alone does not ensure understandable hierarchy.',
 [q('What does proximity usually suggest?','Relatedness','Encryption','Higher server priority',0,'Nearby elements are often perceived as belonging together.'),q('What happens when everything has equal strong emphasis?','Priority becomes harder to scan','Everything becomes equally understandable','The page becomes accessible automatically',0,'Hierarchy requires meaningful differences.'),q('Should visual reordering ignore DOM reading order?','Yes','No','Only on phones',1,'Keyboard and assistive reading paths need a sensible order.')],
 'Group by meaning. Emphasize by task.', ['Primary question','Related groups','Clear hierarchy','Semantic reading order','Scan and keyboard check'], [('WAI page structure','https://www.w3.org/WAI/tutorials/page-structure/'),('NNG visual hierarchy','https://www.nngroup.com/articles/visual-hierarchy-ux-definition/')],usecase='Dense dashboards and responsive ticket pages.',benefits='Reduces search effort without removing needed information.',drawbacks='Grouping can mislead if it implies a relationship the behavior does not honor.',tags=['ux','perception','layout'])

chapter('ux','choices','Choice, memory, and progressive disclosure','beginner',
 'Reduce decision effort while keeping useful options discoverable.',
 '''A menu is a decision problem. Hick–Hyman-style findings relate choice time to uncertainty in controlled tasks. They do not prove that every product should hide options or use exactly a certain number of buttons. Familiarity, grouping, labels, and task frequency matter.

Support recognition instead of forcing recall: show the available statuses, recent queues, or selected filters. Working memory is limited, but “seven items” is not a universal navigation rule. Reduce the information a person must carry across steps.

Progressive disclosure puts common decisions first and exposes less common detail when needed. It works only if people can find the extra options and understand what is hidden. An “Advanced” drawer should not conceal a setting most users need to finish the basic task.''',
 '''```text
Before: 18 unrelated export settings shown at once.
First decision: What do you need? Current results / selected tickets.
Next: Format and destination.
Optional detail: columns, time zone, include archived items.
Summary: “Export 15 selected tickets as CSV, Europe/London.”
```

Keep a visible summary so users do not have to remember earlier choices. Let them change an earlier decision without restarting.''',
 '''Observe where hesitation comes from: too many choices, unfamiliar labels, fear of consequences, or missing information. These need different repairs.

Compare a grouped menu with a flat one using realistic tasks. Measure completion and wrong selections, not only how quickly someone clicks any option. Faster mistakes are not an improvement.''',
 'Hiding every option can increase search and memory burden. A default can help but can also cause a silent wrong choice. Do not use a cognitive “law” as a substitute for context.',
 'A designer cites “seven plus or minus two” to remove three essential navigation items. Give a better decision process.',
 'Identify tasks and information groups, improve labels and organization, and test findability. Consider frequency and recognition. The memory finding is not a hard limit for visible navigation choices.',
 'A power user needs all export options repeatedly. How can the flow avoid becoming slow for them?',
 'Offer remembered presets or a clear compact summary with quick editing. Keep the basic path understandable and make defaults visible. Check that saved choices are still appropriate when scope or permissions change.',
 [q('Is seven a universal maximum for navigation items?','Yes','No','Only for desktop',1,'Visible choices, memory tasks, and navigation contexts differ.'),q('What is the risk of hiding common settings under Advanced?','Lower findability for the basic task','Automatic performance gain','Better authorization',0,'Disclosure should follow task frequency and need.'),q('What should a default make clear?','The choice and its consequences','Only its color','Nothing, because defaults are always safe',0,'Defaults reduce work only when users can understand and change them.')],
 'Less uncertainty, not merely fewer buttons.', ['User decision','Familiar groups','Visible current choices','Optional detail','Result summary'], [('Nielsen recognition and control','https://www.nngroup.com/articles/ten-usability-heuristics/'),('Hick original paper DOI','https://doi.org/10.1080/17470215208416600')],usecase='Export dialogs, status menus, and complex settings.',benefits='Makes choices easier without arbitrarily deleting capability.',drawbacks='Disclosure and defaults can hide important options if poorly chosen.',tags=['ux','cognition','laws'])

chapter('ux','targets','Targets, pointing, touch, and motor effort','beginner',
 'Design controls that are easy to reach and distinguish, beyond making icons larger.',
 '''Fitts’s law connects pointing movement difficulty with target distance and size in a given task. The practical cue is useful: tiny distant targets are often harder to acquire. It does not mean every primary button should fill the entire screen.

The hit area matters, not just the visible icon. Spacing helps users distinguish adjacent actions and avoid accidental taps. Destructive and routine actions should not be indistinguishable neighbors. Keyboard access supplies another path; it does not excuse unusable pointer targets.

Consider touch, mouse, zoom, one-handed use, and limited motor control. A hover-only action can be unavailable on touch and hard to discover. Use WCAG target-size guidance with its exceptions and context rather than treating a single pixel number as the whole usability test.''',
 '''```html
<button type="button" aria-label="Close ticket details" class="icon-button">
  <svg aria-hidden="true"><!-- close icon --></svg>
</button>
```
```css
.icon-button { min-width: 2.75rem; min-height: 2.75rem; padding: .65rem; }
.icon-button:focus-visible { outline: 2px solid currentColor; outline-offset: 3px; }
```

This is one comfortable example, not a universal compliance declaration. Check the actual hit area and nearby controls.''',
 '''Point at the intended target → move → acquire it → confirm the outcome. Watch misclicks and corrective movement. Then complete the same task with keyboard focus and a narrow touch screen.

When a target moves after the user starts pointing because an image loads above it, size alone will not fix the error. Stable layout is part of target reliability.''',
 'A large icon inside a tiny clickable wrapper can still have a small target. A tooltip-only accessible name can be absent for keyboard or touch users.',
 'Close, Archive, and Delete are three tiny adjacent icons with no labels. Propose a safer interaction.',
 'Increase actual target areas and spacing, provide accessible names and discoverable meanings, and separate destructive actions or place them in a clear contextual menu. Keep keyboard focus visible. Test touch and wrong-action recovery.',
 'A dense data table cannot make every control huge. How do you reason about the tradeoff?',
 'Prioritize frequent targets, use row selection and contextual actions, provide keyboard shortcuts with discoverability, and respect target-size/spacing requirements and exceptions. Measure task errors on the actual dense workflow rather than applying a blanket giant-button rule.',
 [q('What matters for pointing besides visible icon size?','Actual hit area and distance','Only color','Only CSS class names',0,'The interactive target is the area users must acquire.'),q('Does Fitts’s law require full-screen buttons?','Yes','No','Only for primary actions',1,'It describes a relationship, not a universal layout prescription.'),q('Why avoid hover-only actions?','Touch and keyboard users may not discover or reach them','They always run slower JavaScript','They disable TLS',0,'Input methods differ.')],
 'Make the intended action easy to hit and hard to confuse.', ['Intended action','Reachable stable target','Clear distinction','Keyboard or pointer input','Visible result'], [('Fitts law in UX','https://www.nngroup.com/articles/fitts-law/'),('WCAG 2.2 target size','https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html')],usecase='Dense toolbars, table actions, and mobile operational screens.',benefits='Reduces avoidable motor errors and missed controls.',drawbacks='Space is limited; target design must balance density and task needs.',tags=['ux','laws','accessibility'])

chapter('ux','feedback','Feedback, errors, undo, and honest progress','intermediate',
 'Design visible system state and recovery for slow, failed, and partially completed work.',
 '''After an action, people need to know whether the system heard them, whether work is still running, and what changed. “Saved” means something different from “Queued.” A progress indicator must describe the boundary it actually observes.

Use a determinate bar only when you know a meaningful total. Use a clear waiting state otherwise. Approximate response-time heuristics can help thinking, but no single threshold fits every network and task. Tell people what they can safely do while waiting.

Prevent predictable errors where possible. For reversible actions, an understandable Undo can be less disruptive than repeated confirmation dialogs. For irreversible or high-consequence actions, make the target and consequence explicit. A confirm dialog that says only “Are you sure?” adds interruption without understanding.''',
 '''```text
Before: “Success!” immediately after an export job is queued.
After: “Export requested. You can keep working.”
Later: “Export ready. Download 15 selected tickets.”
Failure: “Export failed. Your selection is kept. Retry.”
```

For a delete, say “Archive ticket #42?” when archiving is the real operation. Explain where recovery lives and how long it lasts if the product has such a limit.''',
 '''Trace click → acknowledged request → accepted job → processing → result or failure. Map each message to a real backend state. An optimistic UI should explain pending state when the result is not yet confirmed.

For partial success, show successful and failed items separately with a retry policy. Do not make users reconstruct a 50-item selection from memory.''',
 'A spinner with no timeout/recovery can feel abandoned. A percentage based only on elapsed time can be misleading. Toasts that vanish before users read them are poor error storage.',
 'A report button shows “Done” when the queue accepted the request, then the job fails silently. Redesign states and ownership.',
 'Use requested/running/ready/failed states with a durable job ID and status source. Show a retriable failure and preserve the request context. Monitor completion failure in operations too. Do not equate enqueue acceptance with file readiness.',
 'An optimistic archive is reversible but the server rejects it. What should users see?',
 'Restore or reconcile the record, retain context, explain the failed action near where it happened, and offer a safe retry. If the outcome is unknown, check status instead of blindly repeating. Do not leave a disappearing toast as the only evidence.',
 [q('What does queued prove?','The result is ready','The request was accepted for later work','The user downloaded it',1,'Each state has a different completion boundary.'),q('When is a determinate progress bar most defensible?','When a meaningful total and completed amount are known','Whenever a timer exists','Only when green',0,'The percentage should represent observed work.'),q('What makes a confirmation useful?','A clear target and consequence','The phrase Are you sure alone','A second identical button',0,'Users need information to decide.')],
 'Name the real state. Keep a recovery path.', ['Action acknowledged','Pending work','Observed progress','Accurate result','Undo or retry'], [('Nielsen status and errors','https://www.nngroup.com/articles/ten-usability-heuristics/'),('Response-time perspective','https://www.nngroup.com/articles/response-times-3-important-limits/')],usecase='Exports, bulk changes, uploads, and background jobs.',benefits='Builds accurate expectations and supports recovery.',drawbacks='Honest progress needs observable backend states, not only frontend animation.',tags=['ux','feedback','reliability'])

chapter('ux','forms-content','Forms, words, and decision-friendly defaults','intermediate',
 'Write labels, hints, validation, and empty states that help users act correctly.',
 '''Words are interface controls. “Submit” may be less clear than “Assign 15 tickets.” A label names the input; a hint explains a constraint; an error explains what is wrong and how to repair it. Placeholder text is not a stable replacement for a label.

Ask only for information needed now. Explain unusual requirements before users fail. Choose defaults from the task and make their scope visible. A default workspace or audience can create a serious mistake if it is hidden.

Empty, loading, no-results, and failed are different states. “No tickets yet” is not the same as “No tickets match these filters” or “We could not load tickets.” Each needs a different next action.''',
 '''```html
<label for="followup">Follow-up date</label>
<input id="followup" type="date" aria-describedby="followup-help followup-error">
<p id="followup-help">Use the team’s working time zone: Asia/Kolkata.</p>
<p id="followup-error">Choose today or a later date.</p>
```

Render the error only when relevant and keep it associated with the field. For a rejected form, preserve values and provide a useful error summary when several fields need attention.''',
 '''Read the task → understand the field → enter a value → see timely validation → repair if needed → confirm the result. Check whether people understand the terms without internal team knowledge.

For defaults, test changing workspace, returning later, and repeating the action. A remembered choice can become wrong when context changes.''',
 'Required markers without an explanation can be confusing. A disabled button without a reason hides progress. Internal error codes tell users little about the repair.',
 'A page says “No data” for an empty account, zero search results, and a network failure. Write distinct messages and actions.',
 'Empty account: explain what can be created and offer Create ticket. No matches: show active filters and Clear filters. Failure: say loading failed and offer Retry while retaining context. Do not imply the account is empty when the request failed.',
 'A bulk action defaults to notifying all watchers. How can you prevent a hidden surprise?',
 'Show the audience and consequence before the action, make the option easy to inspect/change, and choose the default according to user intent and impact. Test whether users can predict who will be notified without reading a long help article.',
 [q('What should remain visible after typing?','The field label','Only a placeholder','Only an icon',0,'A stable label supports recognition and review.'),q('No matches and load failed should share which message?','An identical No data message','Different messages and recovery actions','A success toast',1,'They describe different states.'),q('What is a good action label?','One that predicts the concrete outcome','Always Submit','An internal method name',0,'The label should help users choose correctly.')],
 'Label the value. Explain the rule. Name the next action.', ['Task language','Label and hint','Input and validation','Preserved values','Specific outcome or repair'], [('WAI forms','https://www.w3.org/WAI/tutorials/forms/')],usecase='Operational forms and bulk actions with meaningful consequences.',benefits='Reduces confusion without adding long tutorials.',drawbacks='Concise language still needs domain accuracy and localization.',tags=['ux','content','forms'])

chapter('ux','inclusive-access','Accessibility as a foundation for usable interaction','beginner',
 'Check semantics, names, focus, contrast, motion, and zoom as part of the main flow.',
 '''Accessibility is not a final color check. A person must be able to perceive the state, operate controls, understand the result, and use compatible assistive technology. Native HTML gives many behaviors that a clickable div does not.

Every interactive control needs an understandable name. Focus must be visible and move predictably. A modal needs a labelled dialog context, a deliberate focus path, and a way to close it. Errors and async status should be announced appropriately without narrating every keystroke.

Use WCAG 2.2 success criteria as requirements to check, with their exact scope and exceptions. Automated tools catch some issues; they cannot tell whether the action name makes sense or whether a real task is understandable. Combine automated checks, keyboard use, zoom, and assistive-technology testing.''',
 '''```html
<button type="button" aria-expanded="false" aria-controls="filters">
  Filters
</button>
<section id="filters" aria-label="Ticket filters" hidden>...</section>
<p role="status" aria-live="polite">15 tickets loaded</p>
```

The application must update expanded and hidden state together. ARIA describes behavior; it does not implement keyboard handling for a custom widget automatically.''',
 '''Complete the same task without a mouse. Can you reach every control, see focus, understand its name, operate it, and recover from failure? Then zoom the page and inspect reflow. Then test the key path with a screen reader.

Respect reduced-motion preferences for unnecessary animation. Avoid information conveyed only by color, hover, or movement.''',
 'Adding role=button to a div without keyboard behavior creates a misleading contract. A focus trap that cannot be escaped is a defect. aria-hidden content can still contain focusable elements if implemented carelessly.',
 'A custom dropdown works with a mouse but not keyboard, and selected state is color-only. Repair the interaction.',
 'Prefer a native select when it meets the task. If a custom widget is necessary, implement the relevant keyboard/focus/ARIA pattern completely and test it. Provide text or state semantics beyond color. Do not add roles without their behavior.',
 'An automated audit reports no errors. What remains to verify?',
 'Meaningful labels, logical task/focus order, keyboard completion, screen-reader experience, errors, zoom/reflow, and dynamic state announcements. A zero-tool-error report is evidence for a limited set of rules, not proof of complete access.',
 [q('Does ARIA implement a custom widget’s behavior?','Yes','No','Only on desktop',1,'ARIA communicates semantics; code still implements interaction.'),q('What is a strong first choice for an ordinary action?','A native button','A clickable span','An image without a name',0,'Native controls supply expected semantics and keyboard behavior.'),q('Does an automated audit prove every task is accessible?','Yes','No','Only with no warnings',1,'Manual task testing is still necessary.')],
 'Name it. Reach it. Operate it. Understand it.', ['Semantic structure','Named controls','Visible focus','Accessible state changes','Task test across input methods'], [('WCAG 2.2 quick reference','https://www.w3.org/WAI/WCAG22/quickref/'),('ARIA authoring practices','https://www.w3.org/WAI/ARIA/apg/')],usecase='Every reusable component and critical business flow.',benefits='Improves access and often clarifies interaction for everyone.',drawbacks='Custom widgets carry ongoing keyboard and semantics responsibilities.',tags=['ux','accessibility','fundamentals'])

chapter('ux','research','Research and metrics: replace confident guesses with evidence','intermediate',
 'Plan a small usability study and interpret product metrics without confusing clicks with success.',
 '''Start with a question: can an agent find and assign the oldest urgent ticket? Give a realistic task without teaching the intended path. Observe hesitation, wrong turns, recovery, and completion. Ask neutral questions; “Was the new button easy?” biases the answer.

Usability sessions reveal problems and reasoning. They do not automatically estimate population-wide percentages. Small samples can find useful issues, but “five users” is not a universal sample-size guarantee. Include people and contexts relevant to the task.

Product analytics records behavior under an event definition. A click is not task success. Define a funnel with a denominator, time window, identity scope, and outcome. Segment carefully. An A/B test needs a decision rule and guardrails; more clicks can mean confusion rather than improvement.''',
 '''```text
Question: Can a new agent hand off overdue tickets correctly?
Task: “Your shift is ending. Move these eligible tickets to Team B.”
Observe: correct selection, audience understanding, partial-failure recovery.
Success metric: correct assignments / eligible handoff attempts.
Guardrail: wrong-team assignments and lost drafts.
```

Use synthetic tasks and minimal event data. Write the event definition before installing an analytics SDK.''',
 '''Hypothesis → task or event definition → collect evidence → distinguish observation from interpretation → choose a repair → test again. Keep quotes and observed behavior separate from your explanation of the cause.

For a funnel, ask who is excluded, whether events can duplicate, and whether missing telemetry correlates with failure. A rising completion rate can reflect a changed denominator rather than a better interface.''',
 'Leading tasks teach the answer. Vanity metrics reward activity without outcome. Changing several things at once makes attribution difficult. Analytics may miss the people who could not even start.',
 'A redesign increases clicks on Assign by 30%, but wrong-team assignments also rise. How should the team assess it?',
 'Examine correct task completion and the error guardrail, not clicks alone. Observe representative tasks to understand confusion. Check event definitions and segments. A higher click count is not sufficient evidence of improvement.',
 'You have only a day for research. What useful small study can you run?',
 'Choose one critical task, a few relevant participants, synthetic realistic data, and neutral prompts. Record where the task fails and why the evidence suggests a repair. Be explicit that qualitative findings are not a precise prevalence estimate.',
 [q('What is a neutral task prompt?','Use the blue Assign button','Hand these overdue tickets to Team B','Tell me why the new design is good',1,'Describe the goal without naming the intended control.'),q('More clicks always mean better UX?','Yes','No','Only in a funnel',1,'Clicks can reflect friction or repeated failure.'),q('What must a completion metric define?','A denominator and outcome','Only a chart color','Only a product name',0,'Without scope, the number is hard to interpret.')],
 'Observe the task. Define the denominator. Keep a guardrail.', ['Question','Neutral task or event schema','Observed behavior','Outcome and error rate','Repair and retest'], [('Usability testing introduction','https://www.nngroup.com/articles/usability-testing-101/'),('Task success metrics','https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/')],usecase='Design reviews, feature experiments, and analytics interpretation.',benefits='Makes UX decisions explainable and revisable.',drawbacks='Small studies and incomplete telemetry have limits.',tags=['ux','research','metrics'])

chapter('ux','review-capstone','A repeatable UX review and redesign workshop','intermediate',
 'Review a workflow using task evidence, interaction principles, accessibility, and measurable outcomes.',
 '''Use your reading of The Design of Everyday Things and Don’t Make Me Think as a starting point, then apply a repeatable review. Look for a mismatch between what users intend, what the interface suggests, what the system does, and what feedback explains.

Separate severity from personal dislike. A lost draft or wrong audience can block or harm the task. A spacing inconsistency may be less urgent. Rate impact, frequency/context, and recoverability with evidence, then state uncertainty.

Create a before/after argument: observed task problem → smallest design change → mechanism expected to help → validation plan. Include empty, slow, failed, partial-success, and permission states. Review the implementation with keyboard, zoom, real data shapes, and realistic wording.''',
 '''```text
Review card
Task: assign overdue tickets during handoff.
Problem: hidden selection persists after filter change.
Consequence: wrong tickets may be assigned.
Repair: visible selected-count scope + inspect/clear selection.
Check: user predicts exactly which tickets will change.
Guardrail: no loss of selection work without explanation.
```

Make a one-page state sketch, not just a polished happy-path mockup.''',
 '''First walk the task yourself. Then inspect controls, grouping, language, feedback, recovery, and access. Then observe another person attempting it. Turn the most consequential finding into a prototype and a focused test.

Keep a small review checklist in daily work: task, context, next action, current state, error prevention, recovery, access, and evidence. Use heuristics to ask questions, not as decorative law names in a design review.''',
 'A beautiful mockup can hide missing system states. A law name does not prove a design. A new interaction can increase learning cost even if it looks cleaner.',
 'A redesign has fewer controls but users cannot find bulk assignment and lose their selection. Write the review card and a better prototype brief.',
 'Name the handoff task, hidden selection scope, lost-work consequence, and discovery failure. Keep a visible contextual action and selection summary, with inspect/clear/recovery behavior. Test prediction of affected items and correct completion before judging visual simplicity.',
 'How will you decide whether the redesign is better after release?',
 'Compare correct task completion, important errors, support reports, and representative observation with stable definitions. Add performance/access guardrails. Check for changed populations or telemetry gaps before claiming causation.',
 [q('What is a persuasive redesign argument?','Problem → mechanism → evidence','A list of law names','Fewer buttons by itself',0,'The reasoning must connect the change to the task.'),q('Which issue is usually more consequential?','Lost user work','A minor decorative inconsistency','A different icon style',0,'Severity depends on impact and recoverability, not taste alone.'),q('What belongs in a state sketch?','Failure and partial success as well as success','Only the final screenshot','Only component names',0,'Real workflows include more than a happy path.')],
 'A principle is a question to test, not a verdict.', ['Task walkthrough','State and access review','Prioritized finding','Small prototype','Outcome evidence'], [('Nielsen heuristics','https://www.nngroup.com/articles/ten-usability-heuristics/'),('WCAG 2.2','https://www.w3.org/TR/WCAG22/')],usecase='Daily frontend reviews and a portfolio-quality workflow redesign.',benefits='Turns UX knowledge into a repeatable engineering/design habit.',drawbacks='A review still needs user and implementation evidence.',tags=['ux','capstone','practice'])
chapter('spring','configuration','Configuration you can explain in every environment','intermediate',
 'Bind and validate configuration, separate secrets, and diagnose which setting actually won.',
 '''Configuration changes behavior without changing the application’s source. That makes it powerful and easy to misunderstand. A value may come from a file, profile, environment variable, command line, or remote source. Record the effective value and its source without logging secrets.

Group related settings with typed configuration rather than scattering string lookups. Validate required URLs, limits, and durations at startup. A service that starts with an invalid payment endpoint can fail much later in a confusing place.

Profiles select groups of behavior; they are not a permission system or a secret store. Prefer workload identity for cloud access and explicit secret injection. Test the production-like configuration graph separately from pure business logic.''',
 '''```java
@org.springframework.boot.context.properties.ConfigurationProperties("receipts")
@org.springframework.validation.annotation.Validated
record ReceiptSettings(
  @jakarta.validation.constraints.NotNull java.net.URI endpoint,
  @jakarta.validation.constraints.Min(1) int maxAttempts) {}
// Enable with @ConfigurationPropertiesScan or @EnableConfigurationProperties.
```
```properties
receipts.endpoint=https://example.invalid/receipts
receipts.max-attempts=3
```

Use a clearly fake endpoint in a training environment. Do not send requests to it as if it were a real provider.''',
 '''Boot prepares environment properties → binds a settings object → validates it → creates dependent clients → starts serving traffic. A bad required setting should fail at a clear boundary.

In a test, supply an invalid max-attempts and verify startup rejects it. Then verify the intended profile chooses the fake integration. A unit test constructing the settings object does not prove binding/validation wiring.''',
 'A default secret committed to a property file is still a secret. A profile name such as prod does not prove that the right database or network was selected.',
 'A service silently uses a local URL in production because a property name was misspelled. Improve the configuration contract.',
 'Use typed grouped configuration, required-value validation, and a wiring test with production-like property names. Expose safe diagnostic metadata, not credentials. Avoid permissive fallback for a setting that must be supplied.',
 'The same container image runs in staging and production. What should differ?',
 'Inject environment-specific endpoints, identities, and secrets at runtime while keeping a reproducible image. Validate each environment’s configuration and permissions. Do not rebuild a secret into separate images.',
 [q('What should a missing required endpoint do?','Fail clearly at configuration validation','Wait until an unrelated request fails','Become a blank URL silently',0,'Early validation localizes the fault.'),q('Does a profile protect a secret?','Yes','No','Only when named prod',1,'Profiles organize settings, not secret access.'),q('What verifies property binding?','A focused context/configuration test','A string comparison in an unrelated unit test','Only a controller mock',0,'Exercise the boundary that binds and validates.')],
 'Bind it. Validate it. Know where it came from.', ['Property sources','Typed binding','Validation','Client wiring','Safe diagnostics'], [('Boot configuration','https://docs.spring.io/spring-boot/reference/features/external-config.html')],usecase='The same service deployed to several environments.',benefits='Clear startup failures and reproducible runtime behavior.',drawbacks='Configuration precedence and secret delivery still need operational ownership.',tags=['spring','configuration'])

chapter('spring','api-contracts','REST contracts: pages, retries, and useful conflicts','intermediate',
 'Design bounded APIs and idempotent command handling with explicit retry behavior.',
 '''An endpoint contract includes more than a URL. Define allowed input, authorization, response shape, errors, ordering, page limits, and retry semantics. A list without a bound can turn an ordinary screen into an accidental bulk export.

Use stable ordering for pagination. Offset pages can shift when rows are inserted; a cursor can be more stable for an append-heavy feed. A cursor must still be scoped to the caller and filter contract.

A retried create can duplicate a ticket. An idempotency key identifies one logical command. Store the key with a request fingerprint and result under a database uniqueness rule. The same key with a different request should conflict. A pre-check in a local map does not protect multiple service instances.''',
 '''```text
POST /tickets
Idempotency-Key: client-generated-command-id
Body: {title, workspaceId}

DB transaction:
  claim unique (actor_scope, command_key)
  compare request fingerprint if already claimed
  create ticket and store response identity
  commit
```

For GET /tickets?after=...&limit=..., cap limit on the server and use a deterministic ordered key. Tokens are data, not authorization.''',
 '''A creates a ticket and commits, but the response is lost. A retry with the same key reads the saved result rather than creating a second ticket. A different payload with that key receives a deliberate conflict.

Test simultaneous same-key requests, a timeout after commit, an invalid cursor, and permission changes. Define key retention; forgetting keys eventually changes retry behavior.''',
 'PUT/POST method names alone do not implement idempotence. Cursor encoding is not encryption or access control. A 200 containing an error object confuses clients.',
 'Two instances both see no idempotency key and create separate rows. Repair the race.',
 'Enforce a unique scoped command key in the database and handle the winner/loser under a clear transaction contract. Store or reconstruct the accepted result and reject conflicting fingerprints. Test independent concurrent transactions.',
 'A list is sorted by mutable priority. What happens to cursor pagination when priority changes?',
 'Rows can move across the cursor boundary. Define snapshot/session semantics or accept and explain possible duplicates/misses, using a stable tie-breaker. If the product requires a stable export, use a snapshot/export job rather than pretending a live list is frozen.',
 [q('What protects a command key across instances?','A database uniqueness rule','A private in-memory Set only','The HTTP method name',0,'The authority must coordinate competing writes.'),q('Same key, different request should usually do what?','Silently return an unrelated result','Produce a deliberate conflict','Create unlimited duplicates',1,'The key identifies one logical request.'),q('What does a bounded list need?','A server cap and deterministic ordering','Only a frontend page size','Only gzip',0,'Clients cannot be trusted to supply safe bounds.')],
 'A retry is the same command only when you can identify it.', ['Validate and authorize','Bound or identify request','Database claim','Commit result','Retry or conflict response'], [('Spring MVC',SPRING+'web/webmvc/mvc-controller.html'),('HTTP semantics','https://www.rfc-editor.org/rfc/rfc9110.html')],usecase='Ticket creation, payment-like commands, and large operational lists.',benefits='Predictable retries and manageable data loads.',drawbacks='Keys, retention, and mutable list ordering need explicit product rules.',tags=['spring','api','idempotency'])

chapter('spring','data-performance','SQL plans, connection pools, and transaction size','intermediate',
 'Investigate a slow service without assuming more threads or caching is the first fix.',
 '''A request can wait for a connection, a row lock, a slow query, or an external service. Low CPU does not prove spare useful capacity. Trace waiting time separately from execution time.

An index should serve a query shape: filter, ordering, and selected data. Check the plan with representative synthetic data and actual predicates. An index adds write/storage cost and may not help a very broad query. Avoid loading full entities when a screen needs a few fields.

A connection pool is a limit, not free throughput. Long transactions hold connections and sometimes locks. Increasing web threads beyond database capacity can grow queues and latency. Keep network calls out of database lock windows when possible.''',
 '''```sql
-- A common bounded work queue query:
SELECT id, title FROM tickets
WHERE workspace_id = 7 AND status = 'open'
ORDER BY created_at, id LIMIT 50;
-- Investigate a matching composite index and EXPLAIN on training data.
```

Use PostgreSQL for PostgreSQL plan/lock claims. The existing H2 lab proves smaller contracts, not the production engine’s plan or concurrency behavior.''',
 '''Trace request arrival → pool wait → SQL/lock wait → row fetch → DTO mapping → response. Measure each boundary before changing a limit.

For a transaction that calls a slow provider between writes, show how many requests can hold connections while waiting. Move delivery intent into an outbox when a later external effect is acceptable.''',
 'A larger pool can overload the database. SQL logs can expose values. A query that is fast on 10 rows may use a different plan on a million.',
 'The app has 200 web threads and 10 DB connections, with 20-second provider calls inside transactions. Explain the likely queue and a repair.',
 'Requests can hold scarce connections while waiting on the provider. Measure pool wait, transaction duration, and provider latency. Shorten the transaction, persist intent, and move safe external work after it. Tune limits from database capacity, not thread count alone.',
 'A new index speeds reads but slows a bulk import. How do you assess the tradeoff?',
 'Measure the read query benefit and write/index maintenance cost on representative workloads. Consider whether the index serves an important query or duplicates another. Plan creation/rollback and database locking carefully.',
 [q('Low CPU and high latency can mean what?','Waiting on a pool, lock, or dependency','There cannot be a bottleneck','Every query is fast',0,'Waiting consumes latency without necessarily consuming CPU.'),q('Does a bigger connection pool always help?','Yes','No','Only with JPA',1,'It can move overload into the database.'),q('Where should PostgreSQL plan claims be verified?','PostgreSQL with representative data','Only a mock repository','Only an H2 happy path',0,'Engine and data distribution affect behavior.')],
 'Find the wait before adding capacity.', ['Request queue','Connection pool','SQL and locks','Short transaction','Measured response'], [('Spring JDBC transactions',SPRING+'data-access/transaction.html'),('PostgreSQL EXPLAIN','https://www.postgresql.org/docs/current/using-explain.html')],usecase='Slow list endpoints and connection exhaustion incidents.',benefits='Repairs the bottleneck rather than hiding it.',drawbacks='Representative measurement and safe database change plans take effort.',tags=['spring','sql','performance'])

chapter('spring','integration-resilience','Remote calls: timeouts, retries, and unknown outcomes','intermediate',
 'Bound dependency work and design retries around a logical command rather than an exception name.',
 '''A remote call crosses a failure boundary. The provider can reject, respond slowly, complete and lose the response, or return malformed data. A timeout says you did not get an answer in time; it does not prove no side effect occurred.

Choose connection/response timeouts and an overall request budget. Limit attempts and use backoff with jitter where appropriate. Retry only failures and operations whose semantics allow it. A circuit breaker can stop repeated pressure on a failing dependency; it does not repair correctness or replace a timeout.

Keep an adapter around the provider so your use case works with a small result contract. Record correlation ID, logical command key, attempt number, duration, and outcome category without logging secrets or whole payloads.''',
 '''```java
interface ReceiptGateway {
  ReceiptResult send(String eventKey, ReceiptRequest request);
}
// Adapter responsibilities:
// configured timeouts; bounded retries; response validation;
// stable provider idempotency key if supported;
// map accepted/rejected/unknown outcomes explicitly.
```

In a fake adapter, record acceptance and then throw a timeout. This reproduces the difficult case without sending real messages.''',
 '''Business change commits with a receipt intent. A worker sends it with eventKey E. The provider accepts E but the response is lost. A retry uses E again under the provider’s documented key contract, or reconciliation resolves uncertainty when such a contract is absent.

Do not retry an entire use case if that repeats unrelated writes. Put the retry around the boundary you actually intend to repeat.''',
 'Nested retries multiply attempts. A 3-attempt client inside a 3-attempt job can make nine calls. A fallback that reports success without performing the required effect is a false result.',
 'A service retries all exceptions around the entire transaction and provider call. Explain two duplication risks.',
 'The transaction may have committed before response loss, and the provider may have accepted before its timeout. Separate local command deduplication, persisted delivery intent, and provider retry semantics. Retry a deliberate boundary with bounded attempts.',
 'The provider has no idempotency key. What can you honestly guarantee?',
 'You can persist intent and track attempts, but a crash between remote acceptance and local acknowledgement leaves uncertainty. Use a provider status lookup/reconciliation if possible, tolerate duplicates where acceptable, or escalate ambiguous outcomes. Do not promise universal exactly-once sending.',
 [q('A timeout proves the provider did nothing?','Yes','No','Only for POST',1,'The outcome may be unknown.'),q('Three nested attempts inside three job attempts can mean how many calls?','3','6','9',2,'Retries can multiply across layers.'),q('What does a circuit breaker replace?','Neither timeouts nor idempotency','Every timeout','All transaction rules',0,'It limits pressure, not the meaning of a repeated effect.')],
 'Bound the wait. Identify the command. Admit uncertainty.', ['Saved intent','Timed adapter call','Accepted or unknown','Bounded safe retry','Reconcile and observe'], [('Spring REST clients',SPRING+'integration/rest-clients.html')],usecase='Email, payments, file conversion, and third-party APIs.',benefits='Contained failure and explainable retry behavior.',drawbacks='Some outcomes remain ambiguous without provider support.',tags=['spring','integration','reliability'])

chapter('spring','modular-usecases','Use-case boundaries and practical modular design','intermediate',
 'Separate transport, business rules, persistence, and external adapters without creating needless layers.',
 '''A use case names an action, such as AssignTicket. It receives validated intent and a trusted actor, checks the rule, coordinates persistence, and returns a result. A controller translates HTTP into that action. A scheduled job can call the same use case through a different entry point.

Put rules near the data and behavior they govern. Do not let a REST controller become the only place ownership is checked if a job or another controller can bypass it. Keep adapters small around SQL and remote services when those boundaries need independent tests.

More interfaces do not automatically mean better architecture. Use a seam when it reduces a real coupling or gives a useful test/failure boundary. Start with a modular monolith when independent deployment is not needed; a network adds partial failure and operations work.''',
 '''```text
ticket/http/AssignController.java   parse + response mapping
ticket/application/AssignTicket.java  trusted actor + transaction
ticket/domain/AssignmentPolicy.java   allowed transition
ticket/persistence/TaskRepository.java SQL access
ticket/integration/ReceiptGateway.java remote boundary
```

Keep module dependencies one-way. Do not expose every entity field as a public API just to save a DTO.''',
 '''Trace the same assignment from HTTP and a background import. Both must enforce the core transition rule. Then replace only the remote receipt adapter with a fake and test the use-case result.

For a new requirement, identify which boundary changes. A new HTTP representation need not rewrite the domain rule. A new provider should mostly change an adapter if its semantics fit the existing contract.''',
 'A service layer that merely forwards every call without a decision may add noise. Distributed services do not remove shared data/contract problems; they move them across a network.',
 'An import bypasses the controller’s ownership and state checks. Repair the boundary rather than copying the same if statements.',
 'Move reusable access/transition rules into the use-case/domain boundary with a trusted actor or explicit system role. Keep HTTP parsing in the controller. Test both callers and reject an invalid transition with no write.',
 'The team proposes five microservices for a small feature. What questions should decide?',
 'Ask about independent change/deployment, team ownership, scaling, data ownership, failure tolerance, and operational capacity. A modular monolith may preserve boundaries with less coordination. Choose networks for a concrete benefit, not a diagram aesthetic.',
 [q('Where should a rule shared by HTTP and jobs live?','A reusable use-case/domain boundary','Only a button handler','Only a controller annotation',0,'Multiple callers must preserve the same core rule.'),q('Do more interfaces automatically improve design?','Yes','No','Only in Java',1,'A seam should address an actual boundary or coupling.'),q('What does splitting a process add?','Network and operational failure boundaries','Automatic consistency','Free deployment safety',0,'Distribution creates work as well as options.')],
 'Name the action. Protect the rule. Isolate real boundaries.', ['Transport input','Trusted actor','Use-case rule','Persistence or adapter','Observable result'], [('Spring application architecture','https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html')],usecase='Features called from controllers, imports, and jobs.',benefits='Rules remain reusable and easier to test.',drawbacks='Unnecessary abstractions can obscure a simple feature.',tags=['spring','architecture'])

chapter('spring','release-testing','Integration tests, migrations, and a release rehearsal','intermediate',
 'Prove the deployed configuration, database changes, and failure recovery beyond mock tests.',
 '''A unit suite can pass while the real application has the wrong bean, migration, permission, or SQL behavior. Keep focused integration tests for the boundaries you rely on. Use a disposable real database when engine behavior matters.

A release changes code, configuration, and sometimes data. Old and new instances may overlap. A migration should remain compatible during that overlap. A code rollback does not restore deleted data or unsend messages.

Rehearse a small release with a known failure. Observe readiness, startup migration ownership, graceful shutdown, in-flight requests, and a rollback decision. A runbook is a short path from symptom to check to safe action to verification.''',
 '''```text
Release rehearsal
1. Start old app against synthetic database.
2. Apply compatible schema expansion once.
3. Start new app and verify critical paths.
4. Simulate provider slowdown and one denied action.
5. Stop new app; verify old app still reads the expanded schema.
6. Record data effects that a code rollback does not reverse.
```

Do not let every app replica independently run a risky long backfill on startup.''',
 '''Build an immutable artifact → verify its configuration → apply a deliberate migration → start and check readiness → send a smoke request → observe → promote or roll back. Keep migration execution separate from ordinary request scaling.

Tests should show both permitted and denied behavior, transaction rollback, and an adapter failure. A green health endpoint alone does not prove the feature works.''',
 'Tests wrapped in a transaction can hide after-commit behavior. A fake repository cannot prove a unique index. A rollback button cannot undo every data effect.',
 'The new app version removes a column while old replicas still read it. Explain a compatible rollout.',
 'Expand first, deploy code that handles both forms, backfill/verify as needed, switch usage, then remove the old field only after old code is gone. Test old/new compatibility on synthetic data and document irreversible steps.',
 'A release passes startup checks but the receipt provider is unreachable. What should the smoke and operations plan show?',
 'Verify bounded behavior, persisted pending intent, useful status, and alerting for backlog/age. Do not declare the feature healthy solely because the process is alive. Decide whether the dependency is required for readiness or handled asynchronously.',
 [q('Does a code rollback undo deleted database rows?','Always','No','Only with a health check',1,'Data recovery is a separate plan.'),q('Who should run a risky backfill?','A deliberate controlled migration/job','Every request thread','Every new replica automatically',0,'Migration work needs coordination and observation.'),q('What does a fake repository not prove?','The real unique index/lock behavior','Local branch decisions','A supplied error mapping',0,'Test the database boundary with the database.')],
 'Test the boundary. Rehearse the release. Separate data recovery.', ['Built artifact','Compatible schema','Configured startup','Smoke and failure tests','Observe or roll back'], [('Spring testing','https://docs.spring.io/spring-boot/reference/testing/index.html'),('Testcontainers PostgreSQL','https://java.testcontainers.org/modules/databases/postgres/')],usecase='A service release with a schema change and background delivery.',benefits='Makes deployment assumptions testable.',drawbacks='Integration environments cost time and still do not cover every production condition.',tags=['spring','testing','delivery'])

chapter('ruby','service-contracts','Rails service objects with a result you can trust','intermediate',
 'Define inputs, results, transaction ownership, and error policy for one Rails use case.',
 '''A service object is ordinary Ruby. It earns its place by naming one use case and making its boundary clear. It does not automatically supply permissions, a transaction, retries, or thread safety.

Choose a result contract. A business rejection such as “already closed” can be an expected result. An unexpected database or programmer error should remain visible to monitoring. Do not rescue everything into nil; callers then cannot tell rejection from failure.

State who owns the transaction and which side effects happen later. Keep request-specific data in arguments and local values. Class-level mutable state can leak across calls or threads.''',
 '''```ruby
# Portable Ruby / Rails 4.2-style service seam.
Result = Struct.new(:ok, :value, :error)
class AssignTicket
  def call(actor:, ticket:, assignee:)
    return Result.new(false, nil, :not_allowed) unless allowed?(actor, ticket)
    Ticket.transaction do
      ticket.update!(assignee_id: assignee.id)
      Result.new(true, ticket.id, nil)
    end
  end
  # allowed? must implement the actual policy; not client-supplied trust.
end
```''',
 '''Controller validates permitted input and identifies actor → service checks the use-case rule → transaction writes → result maps to HTTP. A job caller uses the same rule with a deliberate actor/system role.

Unit-test expected branches with a narrow seam. Use database tests for rollback and constraints. Test the caller’s mapping so a failure is not shown as a success response.''',
 'A service that catches StandardError and returns success hides operational defects. Passing a model from a controller does not mean it belongs to the actor’s tenant.',
 'A service returns nil for not found, not allowed, validation failure, and database outage. Improve the contract.',
 'Separate expected business results from unexpected failures and give callers a small explicit result/error policy. Preserve operational exceptions for monitoring. Test each caller’s visible response and assert no partial writes on failure.',
 'The service is called by an import as well as HTTP. What must be shared and what stays separate?',
 'Share the core permission/transition/transaction rule. Keep transport parsing and presentation outside it. Define the import’s trusted identity explicitly rather than silently bypassing checks.',
 [q('A service object automatically adds a transaction?','Yes','No','Only when named Service',1,'It is ordinary Ruby unless you implement the boundary.'),q('What is wrong with rescuing every failure into nil?','Different outcomes become indistinguishable','It always improves reliability','It validates permissions',0,'Callers lose the failure meaning.'),q('Where should request data live?','Arguments/local variables','Shared mutable class state','A global current ticket',0,'Request ownership should not leak across calls.')],
 'A service name is not a guarantee. Write the contract.', ['Trusted input','Expected rejection','Transaction owner','Explicit result','Caller mapping'], [('Rails transactions','https://api.rubyonrails.org/v4.2.11/classes/ActiveRecord/Transactions/ClassMethods.html')],usecase='A use case shared by controllers and imports.',benefits='Clearer decisions and error handling.',drawbacks='Too many forwarding-only services can add indirection.',tags=['rails','services'])

chapter('ruby','tenant-boundaries','Multi-tenant scopes and object-level permission','intermediate',
 'Keep workspace identity in reads, writes, caches, jobs, and tests.',
 '''Authentication answers who the caller is. A tenant/workspace scope answers which records belong to the current context. Authorization answers which actions are allowed on those records. None replaces the others.

An ID is not proof of access. Load through an allowed scope or enforce a policy before a write. Strong parameters limit fields; they do not establish row access. A job argument must also identify and validate the intended tenant/context.

Caches and analytics are data boundaries too. A cache key missing workspace identity can serve another workspace’s result. Default scopes can hide tenant filtering but are easy to bypass accidentally; make important scope assumptions visible and test them.''',
 '''```ruby
workspace = current_user.workspaces.find(params[:workspace_id])
ticket = workspace.tickets.find(params[:id])
authorize! :update, ticket # example policy integration, if configured
ticket.update!(params.require(:ticket).permit(:title))

# Cache context is part of the key, not permission by itself.
key = "workspace:#{workspace.id}:ticket:#{ticket.id}:v#{ticket.lock_version}"
```''',
 '''Follow the workspace from trusted membership lookup through the record query, policy, service, and result. Repeat the trace for a worker and cached read. Name where revocation takes effect.

Create two synthetic workspaces with colliding local identifiers and users with different roles. Test direct requests and jobs, not only hidden UI buttons.''',
 'A global find followed by a client-supplied workspace ID can authorize the wrong row. Reusing an unscoped cached object can bypass the intended query boundary.',
 'The endpoint is scoped correctly, but a worker uses Ticket.find(id) and a shared cache key. Repair the full path.',
 'Pass/validate workspace context in the job, load within that scope, apply the action policy, and include relevant scope/version in cache keys. Test mismatched job arguments and cross-workspace cached reads. Keep server permission checks independent of cache presence.',
 'A user loses access while a job is waiting. Which policy decision must the product make?',
 'Decide whether the job acts on permissions at request time or execution time, and document any system actor. Recheck current access for sensitive reads/actions as required. Do not accidentally choose by whatever state the worker happens to have.',
 [q('Do strong parameters authorize a row?','Yes','No','Only with a workspace ID',1,'They filter assignable fields.'),q('What belongs in a tenant-scoped cache key?','Relevant tenant and query/version context','Only a global record number','Only the class name',0,'Cache identity must match the data scope.'),q('Must jobs consider permission timing?','Yes, according to an explicit policy','No, jobs are always trusted','Only when they fail',0,'A delayed actor/context can change.')],
 'Carry the scope through every boundary.', ['Trusted workspace','Scoped record','Action policy','Scoped job/cache','Revocation-aware result'], [('Rails controller scopes',RAILS+'action_controller_overview.html'),('Rails security',RAILS+'security.html')],usecase='B2B workspaces and delayed background actions.',benefits='Protects cross-tenant data and makes scope testable.',drawbacks='Implicit context is convenient but easy to lose across jobs and caches.',tags=['rails','security','multi-tenant'])

chapter('ruby','query-plans','Rails queries: indexes, batching, and bounded reports','intermediate',
 'Choose SQL work, Ruby work, and batching with attention to memory and business semantics.',
 '''A report can be correct on ten rows and fail on a million. Ask how many rows are loaded, how many model objects are built, how many queries run, and whether the order matters.

Use SQL filtering/aggregation when it expresses the required rule. Use pluck for selected values when full model behavior is unnecessary. Use batches for large iteration, but check the Rails version’s batching order and limits. Rails 4.2 APIs differ from modern cursor options.

An index serves an actual predicate and order. Check the plan on representative synthetic PostgreSQL data. Avoid assuming an index is used merely because it exists. A large export may need a stable snapshot/job contract rather than paginating a moving live list.''',
 '''```ruby
# Bounded interactive list.
rows = workspace.tickets.where(status: 'open').order(:id).limit(50).pluck(:id, :title)
# Deliberate batch processing in the legacy Rails style.
workspace.tickets.where(status: 'closed').find_each(batch_size: 500) do |ticket|
  rebuild_projection(ticket)
end
```

Do not assume a custom order survives legacy find_each. If the business requires an order, design and test an explicit cursor strategy.''',
 '''Request scope → SQL predicate/order → database plan → limited rows/batches → Ruby transformation → output. Measure rows, query count, and memory at separate points.

For an export, decide what happens when tickets change while it runs. A transaction snapshot may give stability but can be expensive over a long job; a materialized export scope is another tradeoff.''',
 'to_a before filtering moves potentially huge work into Ruby memory. Per-row association reads create N+1. A batch loop that changes its own selection criteria needs a progress rule.',
 'A report loads all tickets, filters in Ruby, then counts by team. Repair the data boundary.',
 'Push allowed scope/filter/grouping into SQL when semantics fit. Select only required fields and bound interactive results. Use an asynchronous export for large output. Verify totals, SQL count, and memory on representative training data.',
 'The batch job marks processed records closed while querying open records. How do you avoid skips or repeats?',
 'Use a stable progress cursor or deliberate claim strategy and define retry idempotence. Test changing rows during iteration. Do not rely on offset pagination over a shrinking set.',
 [q('What can to_a change?','It demands records into memory','It adds a database index','It guarantees a snapshot',0,'Later Ruby filtering may operate on all loaded records.'),q('Legacy find_each always honors custom business order?','Yes','No; check its versioned contract','Only with a model scope',1,'Batching behavior is version-dependent.'),q('What should index choice follow?','The actual predicate/order and measured plan','The longest column name','The controller name',0,'An index is useful for a query shape, not by existence alone.')],
 'Count rows, objects, and queries separately.', ['Scoped relation','SQL plan','Bounded fetch','Batch progress','Measured report'], [('Rails 4.2 queries',RAILS+'active_record_querying.html'),('PostgreSQL plans','https://www.postgresql.org/docs/current/using-explain.html')],usecase='Exports, list screens, and repair jobs.',benefits='Predictable memory and database work.',drawbacks='Batching and snapshot semantics can change the meaning of a report.',tags=['rails','sql','performance'])

chapter('ruby','time-jobs','Time zones, schedules, and jobs that run twice','intermediate',
 'Separate an instant, a local calendar rule, a schedule trigger, and a unique business run.',
 '''“Tomorrow at 9” needs a time zone and a calendar rule. Store an instant for an event that already happened. Store the intended zone/rule as well when scheduling future local-time behavior. Daylight-saving transitions can create missing or repeated local times.

cron or a scheduler triggers work. It does not guarantee exactly one business run. Two schedulers, retries, or a delayed process can trigger the same logical period more than once. Define a unique run key such as workspace plus report date, backed by a database rule.

A job should load current state, tolerate retry according to its contract, and expose a useful outcome. Passing an ID is usually better than serializing a whole model object. A scheduled trigger and a durable work record are different things.''',
 '''```ruby
# Illustrative key: one daily report per workspace calendar date.
run_key = "daily-report:#{workspace.id}:#{local_date.iso8601}"
# Enforce uniqueness in a ReportRun table, then create delivery intent.
# Time.zone helpers must use the intended workspace zone deliberately.
```

Use a fixed test clock and zones with/without DST. Never use the current host timezone as an accidental business rule.''',
 '''Scheduler tick → compute intended business period → claim unique run → snapshot/request work → job retries → durable completion state. If a process crashes after claiming, define how a stale in-progress run is retried or repaired.

Test a late scheduler, duplicate trigger, a DST boundary, and a provider timeout. “It ran yesterday” is weak evidence for these cases.''',
 'A mutex in one Ruby process does not coordinate multiple schedulers. A UTC date and a user-local date can refer to different report periods. A done flag written before the effect can lose work.',
 'Two app replicas each schedule the daily report and customers get duplicates. Repair the business run boundary.',
 'Use one explicit scheduler ownership strategy plus a unique database run key. Make downstream delivery idempotent or reconcilable. Test concurrent triggers and a crash after claim. Scheduler uniqueness alone is not effect uniqueness.',
 'A tenant changes its time zone halfway through a month. What should be defined?',
 'Define which zone applies to past runs, future schedules, and report boundaries. Keep historical instants and relevant scheduling context. Avoid silently reinterpreting past periods using the newest zone setting.',
 [q('What does a schedule trigger guarantee?','Exactly one business effect','Only that work was triggered under its scheduler contract','That mail was delivered',1,'The work needs its own deduplication and completion rules.'),q('What should a business run key identify?','The intended logical period and scope','The worker PID','Only current wall-clock seconds',0,'Duplicate triggers should map to the same logical run.'),q('Does a single-process mutex protect several replicas?','Yes','No','Only in Rails',1,'Its scope is one process.')],
 'A time is not a date. A tick is not a completed run.', ['Calendar rule and zone','Schedule trigger','Unique run claim','Retriable work','Observed completion'], [('Rails time support','https://api.rubyonrails.org/v4.2.11/classes/ActiveSupport/TimeZone.html'),('Sidekiq practices','https://github.com/sidekiq/sidekiq/wiki/Best-Practices')],usecase='Daily reports, reminders, and tenant-local deadlines.',benefits='Prevents common duplicate and off-by-a-day defects.',drawbacks='Calendar changes and ambiguous outcomes need explicit policy.',tags=['rails','time','jobs'])

chapter('ruby','callback-refactor','Refactor callback-heavy Rails without changing behavior accidentally','intermediate',
 'Map hidden effects, move orchestration carefully, and keep a regression timeline.',
 '''Callbacks can protect local lifecycle rules, but they can also hide a large workflow behind save. A concern may register callbacks when included. Search declarations and callers before assuming the method body is the whole behavior.

First map what actually happens: validation, transaction, callback, database write, after_commit, enqueue, and external effect. Rails 4.2 callback halting and exception behavior differ from newer versions; verify the exact fork/version rather than pasting modern throw(:abort) guidance into legacy code.

Move orchestration in small steps. Keep an observed behavior test, introduce an explicit use case, route callers through it, and remove duplicate callback paths only when their coverage is clear. Do not fire the event both explicitly and through the old callback.''',
 '''```text
Before: ticket.save → concern callback → enqueue receipt
Risk: importer + explicit enqueue path may duplicate the effect.

Target: CompleteTicket use case
  transaction: ticket state + one outbox event
  later: dispatcher publishes saved intent
```

Not every callback must disappear. Keep local model rules where their behavior and bypass paths are understood.''',
 '''List entry points and callback registrations. Record one completion with timestamps and event ID. Add tests for update!, bulk updates, imports, and rollback according to their actual paths.

Then change one caller. Assert one logical event, not merely one method invocation under a fake. Inspect direct SQL/bulk methods that intentionally bypass callbacks.''',
 'update_all bypasses model callbacks/validations. A callback’s after_commit hook can still lose enqueue during a crash gap. Removing a callback without tracing callers can remove behavior from an import.',
 'A receipt is sent twice after moving logic into a service while leaving the callback. Propose a safe refactor sequence.',
 'Reproduce the double path, assert one logical event under a unique key, identify all callers, migrate orchestration deliberately, and retire the old effect path. Keep database/event tests and failure timelines. Avoid simply adding another broad rescue.',
 'A bulk maintenance update intentionally skips callbacks. How should the team preserve necessary business effects?',
 'Define whether the maintenance action should create those effects. If yes, use an explicit batch use case/outbox path with idempotent progress. If no, document the intentional bypass and test the state it leaves. Do not assume every SQL update should send user notifications.',
 [q('Where can a callback be registered?','Inside a concern as well as the model','Only in a controller','Only in a migration',0,'Included modules can install lifecycle behavior.'),q('Does update_all run ordinary model callbacks?','Yes','No','Only with a where clause',1,'It is a lower-level bulk update path.'),q('What is a useful regression assertion?','One logical completion event','Only the service class name','A callback exists',0,'The observable effect matters more than the implementation path.')],
 'Map the hidden path before moving it.', ['Find callers and concerns','Observe lifecycle','Protect behavior test','Introduce explicit use case','Remove duplicate path'], [('Rails 4.2 callbacks',RAILS+'active_record_callbacks.html')],usecase='Legacy concerns and duplicate background effects.',benefits='Makes hidden behavior explainable and refactoring safer.',drawbacks='A complete caller map and version-aware tests are necessary.',tags=['rails','legacy','refactoring'])

chapter('ruby','compatibility-tests','Compatibility and boundary tests for a legacy Rails stack','intermediate',
 'Plan a small change or upgrade using version-specific tests rather than broad rewrites.',
 '''Start by recording exact Ruby, Rails, gem, database, and frontend versions. A fork may differ from upstream. A copied snippet is a hypothesis until the relevant boundary test runs in an authorized isolated environment.

Common seams deserve explicit tests: keyword forwarding, autoload/reload, callback order, job serialization, database constraints, request error mapping, and browser component behavior. Keep legacy behavior separate from a deliberate modernized lab.

Characterization tests record what the system currently does. They are useful before refactoring, but do not make a defect desirable forever. Mark a known bad behavior as a decision to change with a new intended contract.''',
 '''```ruby
def delegate(*args, **kwargs, &block)
  target(*args, **kwargs, &block)
end
# Test positional args, explicit keywords including false,
# a final positional hash, and a passed block.
```

The Kafka training app in this course uses Ruby 3.3/Rails 7.2 separately. Its service/outbox ideas can be adapted, but its gem versions and migration syntax must not be pasted unchanged into Rails 4.2.''',
 '''Choose one behavior → record current contract → write a failing/characterization test → make a small change → run affected boundary tests → verify deployment compatibility. Keep a matrix of versions only for the seams actually being changed.

Do not run course experiments inside the work checkout. Use synthetic data and a separately authorized test environment. Private source and data do not belong in the AI tutor.''',
 'A full mock suite can hide broken autoload or SQL behavior. A modern Rails guide can use APIs absent in the old app. A test that merely copies implementation conditions adds little evidence.',
 'A copied modern job example fails on the legacy stack. Diagnose before replacing the queue system.',
 'Check Ruby/gem API requirements, job argument serialization, boot/loading, and transaction timing. Adapt the smallest relevant boundary using versioned docs. Preserve a minimal reproduction and compatibility test.',
 'An upgrade changes a previously optional belongs_to validation default. What is the useful test?',
 'Create/save representative records with and without the association under the old and proposed contract. Decide which behavior is intended, adjust validation/data migration deliberately, and test callers. A green boot alone does not prove model compatibility.',
 [q('Does an upstream version guide prove fork behavior?','Yes','No','Only if the version string matches',1,'Fork changes can alter behavior.'),q('What does a characterization test record?','Current observed behavior','Guaranteed ideal behavior','All production traffic',0,'It supplies a baseline, not a product endorsement.'),q('Should modern lab dependencies be installed into the work checkout for practice?','Yes','No, use a separate training environment','Only without a lockfile',1,'The work project is read-only for this course.')],
 'Record the version. Test the seam. Change one promise.', ['Exact versions','Observed contract','Focused reproduction','Small adaptation','Boundary evidence'], [('Ruby keyword migration','https://www.ruby-lang.org/en/news/2019/12/12/separation-of-positional-and-keyword-arguments-in-ruby-3-0/'),('Rails upgrading',RAILS+'upgrading_ruby_on_rails.html')],usecase='Small legacy changes and planned runtime upgrades.',benefits='Confidence comes from relevant evidence rather than a total rewrite.',drawbacks='A compatibility matrix still has gaps outside tested seams.',tags=['rails','testing','compatibility'])

chapter('git','surgery','Cherry-pick, revert, and moving a fix deliberately','intermediate',
 'Move a small fix between release lines and distinguish patch replay from history preservation.',
 '''Cherry-pick applies a commit’s change onto the current base and usually creates a new commit. It does not bring every dependency of that change automatically. A patch that applies cleanly can still call a helper absent on the release branch.

Revert creates a new corrective commit. It is often easier for collaborators than rewriting a published branch. Reverting a merge requires choosing the intended mainline parent and understanding future merge consequences; do not guess from parent numbers.

Before any history operation, inspect the graph, outgoing patch, and current work. Use a disposable worktree for a release rehearsal. Record which release line received the fix and how it was tested there.''',
 '''```sh
git show <fix-id> --stat
git show <fix-id>
# In a clean, deliberate release-fix branch/worktree:
git cherry-pick <fix-id>
# On conflict, inspect intent, then continue or abort:
git cherry-pick --abort
```

Replace placeholders with inspected IDs. Do not execute these commands in an unrelated active checkout.''',
 '''Fix on main → inspect dependencies → replay onto release branch → resolve intent → test release configuration → review. The new commit ID can differ even when the patch is similar.

For a revert, test the resulting behavior with later changes present. A reverse patch is not a reversal of every external effect or migration.''',
 'A clean cherry-pick can be behaviorally incomplete. Reverting a migration commit does not reconstruct deleted data. Shared branch rewrites need coordination.',
 'A hotfix cherry-picks cleanly but fails because a helper was introduced in an earlier main commit. Repair the release plan.',
 'Identify the minimal dependency or adapt the fix to the older contract. Test the actual release branch in a clean worktree. Avoid dragging a large unrelated feature into the release just to obtain a helper.',
 'A bad merge is already shared. What must be inspected before reverting it?',
 'Inspect both parents, the intended mainline, later dependent changes, and the resulting behavior. Explain how the revert affects future merges. Preserve shared ancestry and test the corrective patch.',
 [q('Does cherry-pick copy a whole branch dependency graph?','Yes','No','Only if clean',1,'It replays the selected change, not every dependency.'),q('A clean application proves what?','Text applied, not full behavioral correctness','All tests passed','Data was restored',0,'Behavior still needs verification.'),q('What makes a release-fix test relevant?','Running on the actual release base/configuration','Only running main tests','Only checking the commit title',0,'The older base may have different contracts.')],
 'Move the patch. Check its assumptions.', ['Inspect fix','Check release base','Replay change','Resolve dependencies','Test target release'], [('Git cherry-pick','https://git-scm.com/docs/git-cherry-pick'),('Git revert','https://git-scm.com/docs/git-revert')],usecase='Backports and shared-history repairs.',benefits='Small fixes can move without unrelated features.',drawbacks='Dependencies and merge semantics can make a small patch nontrivial.',tags=['git','releases'])

chapter('git','conflict-lab','Conflicts are behavior decisions','intermediate',
 'Resolve a conflict by comparing base and both intents, then test the combined rule.',
 '''Conflict markers identify text Git could not combine automatically. They do not tell you which product behavior should win. Read the common base, each change, callers, and tests.

During rebase, Git replays your commits onto another base. The meanings of ours and theirs can feel reversed from an ordinary merge. Inspect actual content rather than clicking a side label by habit.

Some dangerous conflicts are semantic and have no markers: one change renames a field while another still sends the old field; one adds a new state while another assumes only two states. Test the combined contract even after a clean merge.''',
 '''```sh
git status
git diff
git show :1:path/to/file  # common base, when present in an unmerged index
git show :2:path/to/file  # one side
git show :3:path/to/file  # other side
```

In a scratch repository, make one branch add authorization and another refactor the method. The final code must preserve both the new structure and the permission rule.''',
 '''Write intended before/after behavior for each branch. Decide the combined behavior. Edit the resolution, stage it, continue the operation, and run the relevant regression tests. If the operation is wrong for the task, abort deliberately after preserving needed work.

Use the graph to explain where the resolution lives. A merge commit can contain meaningful hand-written conflict decisions that deserve review.''',
 'Accept Both can duplicate work or create unreachable code. Accept Current can remove a new rule. Conflict-free text can still be an invalid combined design.',
 'A conflict resolution keeps a refactor but drops a newly added access check. Write a repair and regression test plan.',
 'Recover both intended changes from the base/sides, restore the access rule in the refactored path, and test allowed/denied cases. Review the resolved patch rather than only checking that markers disappeared.',
 'A clean merge changes an API field name on one side but not its caller. How would you catch it?',
 'Run a contract/integration check for the connected caller and endpoint. Search call sites and inspect both changes’ intent. Textual success is not API compatibility.',
 [q('What does removing conflict markers prove?','Only that the markers are gone','The intended behavior is preserved','All dependencies match',0,'The combined rule needs review and tests.'),q('Why inspect base and both sides?','To recover each change’s intent','To choose the newest timestamp automatically','To avoid all tests',0,'Conflict resolution is a behavior decision.'),q('Can a clean merge be semantically wrong?','Yes','No','Only with binaries',0,'Git merges text, not business rules.')],
 'Keep both intentions when both are still valid.', ['Common base','Intent on each side','Combined rule','Resolved patch','Behavior test'], [('Git merge','https://git-scm.com/docs/git-merge'),('Git rebase','https://git-scm.com/docs/git-rebase')],usecase='Refactors overlapping feature and access changes.',benefits='Preserves meaning rather than merely producing parseable text.',drawbacks='The correct answer may require a product/API decision.',tags=['git','practice','conflicts'])

chapter('git','investigation-practice','Reflog, bisect, and exact-snapshot investigation','intermediate',
 'Combine recovery and regression search without destroying unrelated working edits.',
 '''Use reflog to find a recent local reference movement, then name the candidate commit with a rescue branch before changing anything else. Reflog is local and expires; it does not store every unsaved file.

Use bisect only after a repeatable good/bad check exists. A flaky network dependency can make a confident wrong culprit. Verify the check against known endpoints of the search.

A worktree gives a separate checkout for the exact committed snapshot. It helps avoid accidentally testing a staged patch together with unstaged helper changes. Save needed files before removing a worktree, and use Git’s worktree commands to keep registration consistent.''',
 '''```sh
git reflog -10
git show <candidate-id> --stat
git branch rescue/investigation <candidate-id>
git worktree add --detach ../ticket-investigation <candidate-id>
# Run the repeatable test there, then inspect its result.
git worktree list
```

Use a fresh scratch location. A detached worktree is suitable for inspection; create a deliberate branch if you intend to keep new commits.''',
 '''Observed regression → minimal deterministic check → known-good/bad commits → bisect or exact-snapshot comparison → inspect trigger → preserve regression test. Keep the active worktree’s edits untouched.

A first-bad dependency update is a trigger to investigate, not automatically the root explanation. Reproduce the mechanism after locating the change.''',
 'A test can fail because its historical build environment is unavailable. Mark such commits untestable/skip rather than bad. A cleanup command can delete untracked work that Git never stored.',
 'An engineer uses reset --hard to prepare for bisect and loses unrelated edits. Describe a safer workflow.',
 'Inspect and preserve active work first. Use a separate worktree for the investigation, with a repeatable check and clear good/bad states. Do not use destructive cleanup as a generic preparation step.',
 'The historical commit cannot install a removed dependency. What should the bisect report say?',
 'Treat it as untestable unless the failure is the regression being investigated. Use skip or a controlled compatible environment and report uncertainty. Do not label a build-environment failure as proof of the product bug.',
 [q('Reflog recovers every unsaved file?','Yes','No','Only on main',1,'It tracks local ref movements, not arbitrary editor contents.'),q('What makes bisect trustworthy?','A repeatable classification check','A large repository','A clean commit message style',0,'Its result depends on correct good/bad evidence.'),q('Why use another worktree?','Test a committed snapshot while preserving active edits','Create a second remote automatically','Make all tests faster',0,'It isolates working files and index from the active checkout.')],
 'Preserve work. Reproduce the symptom. Search the graph.', ['Active edits preserved','Separate checkout','Stable test','Candidate change','Explained regression'], [('Git reflog','https://git-scm.com/docs/git-reflog'),('Git bisect','https://git-scm.com/docs/git-bisect'),('Git worktree','https://git-scm.com/docs/git-worktree')],usecase='Regression investigations and accidental branch movements.',benefits='Evidence without sacrificing unrelated work.',drawbacks='Historical environments and expired objects limit recovery/search.',tags=['git','debugging','practice'])

chapter('git','team-release','A practical Git release and review routine','intermediate',
 'Review a change, integrate upstream work, and preserve a traceable release without rewriting shared history casually.',
 '''Before review, compare against the intended base and inspect the actual outgoing patch. Explain the trigger, resulting behavior, test evidence, and known limitation. A long commit list is not a substitute for that explanation.

Fetch updates your remote-tracking knowledge. Integration is a separate decision. A rejected push means the remote state changed; inspect before deciding how to integrate. force-with-lease is a check against an expected tip, not permission to surprise collaborators.

For a release, name the exact commit/artifact, schema compatibility assumptions, and rollback/data-recovery plan. Keep hotfix backports traceable. A Git tag names a version but does not prove the deployed container matches it; connect it to an image digest or build record.''',
 '''```sh
git fetch origin
git log --oneline origin/main..HEAD
git diff --stat origin/main...HEAD
git diff origin/main...HEAD
git status --short
```

Do not publish, tag a shared release, or rewrite shared branches as an automatic course exercise. Practice the graph in a disposable local remote.''',
 '''Reviewable branch → fetch and compare → relevant tests → reviewed integration → immutable build identity → release observation. Keep the relation between source revision and deployed artifact visible.

Use small commits that can be understood and, when necessary, reverted meaningfully. Separate a mechanical rename from a behavior change when that improves review.''',
 'A tag can be moved unless policy protects it. A branch diff on the wrong base can hide important changes. A passing working-tree test may include uncommitted content.',
 'A team says release v2 is deployed, but the image was rebuilt from an uncommitted tree. Repair traceability.',
 'Build from an identified clean source revision in a controlled pipeline, record the image digest, and deploy that immutable artifact. Preserve provenance and the validation result. A version label alone cannot reconstruct uncommitted source.',
 'Your push is rejected after a teammate’s update. What routine should replace force by habit?',
 'Fetch, inspect divergence and incoming changes, integrate by the team’s policy, resolve/test, then push normally. Coordinate any intended rewrite explicitly. Preserve work before changing the graph.',
 [q('Does force-with-lease replace team coordination?','Yes','No','Only for release branches',1,'It checks remote state, not collaborator expectations.'),q('What should a deployment identify?','Exact source revision and artifact digest','Only a friendly branch name','Only the latest tag text',0,'Mutable names alone are insufficient provenance.'),q('What should a review description lead with?','The problem and resulting behavior','Every shell command run','The number of changed lines',0,'Reviewers need the behavior and evidence.')],
 'Review the patch. Release the artifact. Keep the link.', ['Intended base','Reviewable patch','Validated commit','Immutable artifact','Observed release'], [('Git fetch','https://git-scm.com/docs/git-fetch'),('Git push','https://git-scm.com/docs/git-push')],usecase='Collaborative feature delivery and release support.',benefits='Understandable changes and traceable deployments.',drawbacks='Tools cannot substitute for team policy and review.',tags=['git','delivery','practice'])
chapter('cloud','identity','AWS identity: accounts, roles, and the caller you actually are','beginner',
 'Set up a training identity and distinguish human sign-in, workload roles, trust, and permissions.',
 '''An AWS request is made by a principal under a permission context. Human sign-in and application identity should be separate. Use a dedicated training account/profile and temporary credentials. A workload normally receives a role instead of a permanent access key baked into its image.

A role has a trust policy describing who may assume it and permission policies describing allowed actions/resources. Both matter. An explicit deny or an organizational boundary can still block an apparently allowed action. Region and account are part of your context.

Setup path: establish the training account and human SSO/federation flow, configure a named CLI profile, verify caller identity and region, create a narrowly scoped workload role, and test an allowed and denied operation. Budget alerts help notice spend; they are not a hard spending cap.''',
 '''```sh
# Read-only checks, using your deliberately configured training profile.
aws sts get-caller-identity --profile learning
aws configure get region --profile learning
```
```ruby
require 'aws-sdk-s3'
s3 = Aws::S3::Client.new(region: ENV.fetch('AWS_REGION'))
# The SDK credential provider chain supplies identity.
# Do not embed access keys in this source.
```

No AWS commands or resource creation run automatically from this course.''',
 '''Human signs in → temporary credentials identify a principal → workload assumes its permitted role → SDK signs a request → AWS evaluates action/resource/context → result or denial. For an AccessDenied, record the caller ARN, action, resource, and request ID without secrets.

For ECS, distinguish the task role used by app code from the execution role used for platform tasks such as image/secret retrieval. In EKS, use the supported pod identity mechanism rather than giving every pod the node’s broad privileges.''',
 'A correct region with the wrong account can still target the wrong resource. Administrator access can make a lab pass while hiding the permission you actually need.',
 'A Rails container can start but S3 calls are denied. What identity and policy checks come first?',
 'Verify the app’s actual workload caller, account, region, action, bucket/key ARN, role trust, and effective allow/deny context. Do not solve it by adding administrator permissions. Test one narrow allowed key and a denied outside prefix.',
 'The same image moves from a laptop to ECS. How should credentials change?',
 'Keep code using the SDK provider chain. Use the configured temporary development identity locally and an ECS task role in the workload. Keep execution-role responsibilities separate. No secret rebuild is needed.',
 [q('What does a role trust policy answer?','Who may assume the role','Which CSS theme is active','Which SQL query is fastest',0,'Trust and action permissions are separate.'),q('Are budget alerts a hard spending cap?','Yes','No','Only for EC2',1,'Alerts notify; they do not universally stop spending.'),q('Where should a container’s AWS keys normally live?','Use workload role credentials, not baked keys','In the Dockerfile','In committed source',0,'Temporary workload identity avoids embedded long-lived keys.')],
 'Who calls? What action? Which resource? Under which context?', ['Training account','Human or workload identity','Role trust','Action and resource policy','Verified request'], [('IAM practices',AWS+'IAM/latest/UserGuide/best-practices.html'),('Ruby credential chain',AWS+'sdk-for-ruby/v3/developer-guide/credential-providers.html')],usecase='Every Rails-to-AWS integration.',benefits='Explicit identity and smaller permission scope.',drawbacks='Several policy layers can affect the final decision.',tags=['aws','iam','setup'])

chapter('cloud','networking','VPC networking: follow the packet','beginner',
 'Trace public ingress, private application traffic, database access, and outbound AWS calls.',
 '''A VPC is a network boundary you configure. A subnet belongs to one Availability Zone. A route table decides where traffic goes. A security group controls allowed traffic for attached resources; a route and a permission rule solve different parts of connectivity.

“Private subnet” does not mean an application has no outbound needs. A worker may need S3, a queue, image registry, or an external email API. NAT and VPC endpoints are different ways to reach services, with different scope and costs. Choose the path you need; do not add a NAT gateway by reflex.

Setup sketch: choose non-overlapping CIDRs, subnets in two zones, explicit route tables, an internet-facing load balancer where needed, private app/database placement, and security-group references that allow only the intended paths. Record DNS resolution and outbound service access.''',
 '''```text
Internet → public ALB :443
ALB security group → Rails task security group :3000
Rails task security group → RDS security group :5432
Rails → S3 endpoint or deliberate outbound path
Worker → permitted provider endpoint
```

This is a design/configuration checklist. Verify the chosen endpoint, DNS, routes, and group rules in your training account before running a workload.''',
 '''A request needs DNS, a routable destination, a listener, and allowed traffic. A database timeout is not the same as a database login rejection. Follow the packet one hop at a time.

For S3 from a private task, inspect the endpoint/NAT route, endpoint policy, task IAM role, and bucket policy. Network reachability does not imply S3 authorization.''',
 'Putting RDS in a subnet does not decide all access rules. Opening a group to the whole internet can hide a wrong source rule. A NAT gateway can add continuing cost and is not inbound access to a private task.',
 'Rails times out reaching PostgreSQL after moving into a VPC. Create a layered investigation.',
 'Check resolved address, subnet route path, source/destination security groups, NACLs if customized, database listener/health, then credentials/TLS. Distinguish timeout from authentication error. Change the smallest broken boundary rather than opening every port.',
 'The task reaches the DB but cannot pull an image or call S3. What was missing from the network model?',
 'Startup and outbound dependencies need paths too. Model registry/auth/logging/secrets and application calls with appropriate endpoints or controlled egress. Check IAM separately. A DB path alone is not a complete workload network.',
 [q('A subnet belongs to how many Availability Zones?','One','Every zone in a region','All regions',0,'A subnet is an AZ-scoped network range.'),q('Does a route table authorize S3 object reads?','Yes','No','Only through NAT',1,'Routing and IAM/resource policy are separate.'),q('What is NAT primarily useful for here?','A deliberate outbound path for private workloads','Universal inbound access','Database row locking',0,'NAT is not a substitute for every other network/security boundary.')],
 'DNS → route → listener → allowed traffic → application permission.', ['Name resolution','Subnet route','Security-group path','Service listener','Application result'], [('VPC overview',AWS+'vpc/latest/userguide/what-is-amazon-vpc.html')],usecase='Private Rails tasks with RDS and AWS service calls.',benefits='Makes timeouts and access boundaries explainable.',drawbacks='Egress, endpoints, zones, and policy add operational choices and cost.',tags=['aws','vpc','networking'])

chapter('cloud','ec2','EC2 and EBS: when you own the machine','beginner',
 'Explain instance lifecycle, disk persistence, process supervision, and the responsibilities EC2 leaves with you.',
 '''EC2 gives you virtual machines. You choose an image, instance capacity, network, identity, and storage. You still own operating-system patching, process configuration, application deployment, and much of the recovery plan.

An instance is not the same thing as a persistent data store. EBS volumes have their own lifecycle and zone attachment rules; instance-store data is a different contract. A Rails app should not treat its local upload directory as shared storage across several instances.

Training setup: select a deliberate image/type, attach a narrow instance role, use controlled management access, configure security groups, supervise the app process, send logs off the machine, and test replacing the instance. Keep the database and uploads in services with explicit persistence/backup policies.''',
 '''```text
EC2 process responsibility map
OS/service manager → starts and restarts Rails/Puma
Instance role → AWS API permissions
EBS → deliberate filesystem persistence
RDS → relational source of truth
S3 → shared attachment objects
```

For a demo, document what is lost if the instance is terminated and which volume deletion settings apply. Do not infer persistence from one reboot.''',
 '''Boot image → inject configuration/identity → start supervised process → health check → receive traffic. Replacement should recreate the application from its artifact/configuration, not depend on manual edits left on the old machine.

Scale to two instances and follow an upload/read. If only one instance has the file, the storage boundary is wrong for that architecture.''',
 'A manually repaired server becomes hard to reproduce. A successful reboot is not a tested restore. Local logs disappear with the machine if not collected.',
 'Two Rails instances behind a load balancer intermittently return missing uploads. Repair the storage design.',
 'Store shared objects in S3 or another deliberate shared storage service, retain metadata/permissions in the DB, and avoid instance-local upload assumptions. Test a read from either instance and replacement of one instance.',
 'When might EC2 still be a reasonable choice over managed containers?',
 'When machine-level control, a specific runtime/agent requirement, or an existing operational model provides a concrete benefit. Compare patching, scaling, deployment, and recovery effort rather than assuming a VM is automatically simpler or cheaper.',
 [q('What responsibility remains with EC2 users?','OS/application operation choices','None','Only HTML styling',0,'A VM does not manage the whole application lifecycle.'),q('Is a local upload directory shared across EC2 replicas?','Automatically','No','Only if file names match',1,'Storage must be deliberately shared or externalized.'),q('What should replacement rely on?','Reproducible artifact and configuration','Manual undocumented edits','The old machine never failing',0,'Recovery should not depend on a pet server.')],
 'A machine is replaceable only if its important state is accounted for.', ['Image and instance','Identity and config','Supervised process','External durable state','Replacement test'], [('EC2 concepts',AWS+'AWSEC2/latest/UserGuide/concepts.html'),('EBS overview',AWS+'ebs/latest/userguide/what-is-ebs.html')],usecase='Understanding existing VM deployments and choosing compute ownership.',benefits='Flexible machine-level control.',drawbacks='Patching, configuration drift, and recovery remain your work.',tags=['aws','ec2','storage'])

chapter('cloud','load-balancing','Application Load Balancer: traffic is a separate layer','beginner',
 'Configure listeners, target health, and request routing without confusing liveness with readiness.',
 '''An ALB accepts HTTP(S) traffic and forwards it according to listeners/rules to target groups. The target group knows where application targets live and how health is checked. A listening app port alone does not prove the app should receive traffic.

TLS termination, forwarded headers, idle timeouts, and target health affect Rails behavior. Configure trusted proxy/host handling deliberately. A bad redirect rule can create an HTTPS loop when the app misinterprets the original scheme.

Setup: create the ALB in suitable subnets, attach an allowed ingress group, add an HTTPS listener/certificate, create a target group with the correct app port and readiness path, allow only the ALB-to-app path, register targets, and observe a request and a failed target.''',
 '''```text
Listener :443 → target group tickets-web
Target port :3000
Health path /ready
Healthy means: this instance can accept the intended traffic now.
```

Keep /live as a narrower process-health concept if you need it. Do not make every unrelated external provider failure trigger a restart loop.''',
 '''Client connects → TLS listener → routing rule → healthy target → Rails → response. On a 502/503/504, identify whether there were no healthy targets, a connection/protocol issue, or a slow target/dependency.

During deployment, allow draining and graceful shutdown so an old target can finish appropriate in-flight work before termination.''',
 'A health path that requires user login can mark every target unhealthy. A constant OK may hide failed startup dependencies. Sticky sessions can conceal session/storage assumptions rather than repair them.',
 'The ALB reports no healthy targets, but curl on the container port works. What do you inspect?',
 'Check target port/protocol, health path/status expectations, authentication on that path, security-group source, registration, and startup readiness timing. A local curl does not test the ALB-to-target route.',
 'Long exports time out behind the load balancer. What design change may be better than increasing every timeout?',
 'Use an accepted export job with a status endpoint and later S3 download when product semantics allow it. Bound the request path and make job completion observable. Adjust timeouts deliberately for the actual interaction.',
 [q('What decides which app targets receive traffic?','Target health and routing rules','The Docker image name only','The database primary key',0,'Traffic routing is an explicit layer.'),q('Should readiness always be a constant OK?','Yes','No, it should reflect the chosen traffic-readiness contract','Only on ECS',1,'The health signal must mean what operators think it means.'),q('A local curl proves ALB network access?','Yes','No','Only over HTTP',1,'It bypasses the load-balancer path.')],
 'A running process is not automatically a ready target.', ['HTTPS listener','Routing rule','Healthy target group','Rails request','Drain or observe failure'], [('ALB introduction',AWS+'elasticloadbalancing/latest/application/introduction.html')],usecase='Public Rails traffic and rolling deployments.',benefits='Central traffic routing and health-based distribution.',drawbacks='Proxy headers, timeouts, and health contracts need configuration.',tags=['aws','alb','networking'])

chapter('cloud','dns-tls','Route 53 and ACM: names and trust before the request','beginner',
 'Explain DNS records, certificate validation, region constraints, and what a DNS change does not instantly control.',
 '''DNS resolves a name to a destination. It does not forward each HTTP request through a Rails controller. Route 53 can manage DNS records and health/routing policies. Cached answers mean a record change is not an instantaneous global traffic switch.

TLS certificates connect a name to a trusted identity under certificate rules. ACM can manage supported certificates, but you still configure validation and attach the certificate to the right service. Services can have specific certificate-region requirements; verify those for ALB versus CloudFront.

Setup: own/control the domain, establish the hosted zone and registrar delegation, create/validate the certificate, attach it to the selected listener/distribution, create the deliberate alias/record, and test DNS plus HTTPS separately. Keep domain renewal and validation records in the ownership map.''',
 '''```text
Name tickets.example.invalid
DNS record → selected ALB/CloudFront destination
Certificate → covers the exact intended hostnames
HTTPS service → presents that certificate
Rails → validates allowed hosts/proxy context
```

Use an actual controlled training domain only when you choose to provision. example.invalid is a placeholder, not a working deployment target.''',
 '''Resolver asks DNS → caches an answer → browser connects to that destination → TLS verifies hostname/certificate → HTTP request begins. A certificate error is different from NXDOMAIN or a target timeout.

For cutover, plan existing cache lifetimes, overlapping service readiness, rollback, and certificate coverage. DNS is one part of the release, not the whole release mechanism.''',
 'A certificate for one hostname does not cover arbitrary other names. Creating a hosted zone without registrar delegation may not affect public resolution.',
 'The app works by direct ALB hostname but the custom name fails. Diagnose in layers.',
 'Check delegation and record resolution first, then certificate hostname/validation/attachment and HTTPS listener, then allowed-host/proxy configuration. Distinguish DNS failure, TLS failure, and application rejection.',
 'The team wants a DNS flip to roll back every user instantly. What limit must be explained?',
 'Resolvers and clients may retain cached answers. Keep both destinations safe during the transition and use a controlled traffic strategy when immediate routing control is required. DNS TTL is not a universal instant rollback switch.',
 [q('Does DNS normally proxy each HTTP request?','Yes','No','Only with an alias',1,'It supplies name-resolution answers.'),q('A hosted zone alone proves public delegation?','Yes','No','Only with ACM',1,'The registrar/delegation chain must point to it.'),q('What must a certificate match?','The requested hostname under its rules','Only the EC2 instance ID','Only the Rails environment',0,'TLS hostname validation is separate from app routing.')],
 'Resolve the name. Verify the name. Then handle HTTP.', ['Domain delegation','DNS answer','TLS name validation','HTTPS endpoint','Application host context'], [('Route 53 overview',AWS+'Route53/latest/DeveloperGuide/Welcome.html'),('ACM overview',AWS+'acm/latest/userguide/acm-overview.html')],usecase='Custom domains and reliable traffic cutovers.',benefits='Managed names and supported certificate lifecycle.',drawbacks='Caching, validation, service scope, and renewal ownership still matter.',tags=['aws','dns','tls'])

chapter('cloud','s3','S3 for Rails attachments: private objects and signed access','intermediate',
 'Set up private object storage and trace metadata, upload, authorization, and download separately.',
 '''S3 stores objects addressed by bucket and key. A slash in a key is a naming convention, not a filesystem directory with ordinary POSIX behavior. Keep application metadata and access rules in the database; the object is the bytes.

Use private defaults and a workload role scoped to the required bucket/prefix/actions. A presigned URL grants time-limited access using the signer’s permissions. It can be reused while valid and may expire earlier when its credentials expire. It is not inherently a single-use ticket.

Setup: choose a unique training bucket/region, block unintended public access, choose encryption and lifecycle/versioning deliberately, scope the app role, configure CORS only for required browser direct-upload behavior, then test an allowed upload/read and denied outside key. Plan cleanup of abandoned uploads and retained versions.''',
 '''```ruby
require 'aws-sdk-s3'
client = Aws::S3::Client.new(region: ENV.fetch('AWS_REGION'))
signer = Aws::S3::Presigner.new(client: client)
# Authorize the caller and resolve the allowed key on the server first.
url = signer.presigned_url(:get_object,
  bucket: ENV.fetch('ATTACHMENT_BUCKET'),
  key: "workspaces/7/tickets/42/attachment-uuid", expires_in: 300)
```

Use generated object identities, deliberate content rules, and post-upload validation. A successful PUT does not automatically create the correct Rails metadata row.''',
 '''User requests attachment → Rails authorizes record → app issues allowed key/URL → browser uploads bytes → app verifies completion and saves metadata → later read rechecks access before issuing a download.

Test the crash between upload and metadata save. Orphan cleanup must distinguish abandoned objects from live references. For immediate revocation needs, consider the lifetime of already issued URLs.''',
 'A public bucket can bypass Rails permission checks. Reusing a key can replace an existing object according to the operation/versioning contract. A presigned URL should not be logged as harmless metadata.',
 'A user supplies any S3 key to a download endpoint and receives a signed URL. Repair the authorization path.',
 'Load an allowed attachment record from the caller’s scope and derive its stored key server-side. Never sign arbitrary user-selected keys. Keep the bucket private and test cross-workspace/key attempts. Consider already issued URL lifetime on revocation.',
 'Upload succeeds but the browser closes before metadata save. How do you recover?',
 'Use a pending-upload record or explicit completion flow and reconcile unreferenced objects after a safe window. Validate object properties and ownership before making it visible. Track cleanup and retained versions deliberately.',
 [q('A presigned URL is inherently single-use?','Yes','No','Only with GET',1,'It can be used while its permission and expiry remain valid.'),q('Where should allowed download keys come from?','An authorized server-side attachment record','Any key typed by the browser','A public bucket listing',0,'Signing a key is an access decision.'),q('Does storing bytes prove Rails metadata was saved?','Yes','No','Only for small files',1,'Those are separate writes/boundaries.')],
 'DB owns permission and meaning. S3 owns bytes.', ['Authorized metadata','Allowed object key','Signed upload or read','Object verification','Reference and cleanup'], [('S3 guide',AWS+'AmazonS3/latest/userguide/Welcome.html'),('Presigned access',AWS+'AmazonS3/latest/userguide/using-presigned-url.html')],usecase='Private attachments and generated reports.',benefits='Shared durable object storage without app-local upload disks.',drawbacks='Metadata consistency, URL lifetime, lifecycle, and transfer costs need design.',tags=['aws','s3','rails'],lab='aws-rails')

chapter('cloud','cloudfront','CloudFront: fast delivery without mixing private users','intermediate',
 'Choose cache keys, origin access, and freshness rules for assets and authorized downloads.',
 '''CloudFront is an edge delivery/cache layer in front of an origin. Static versioned assets are a natural fit. Dynamic or personalized responses require a deliberate cache key and authorization policy.

Cache identity answers which requests may share a response. If two users receive different data but the key omits that difference, a shared cache can leak content. Do not solve this by forwarding every header blindly; that can destroy cache usefulness and complicate origin behavior.

Setup: select an origin, restrict direct S3 origin access when appropriate, create behaviors for assets versus dynamic paths, choose cache/origin-request policies, configure TLS/domain, and test hit/miss plus a private-user boundary. Version asset names to avoid expensive broad invalidations for every release.''',
 '''```text
/assets/app.<content-hash>.js → long-lived immutable asset behavior
/api/tickets → deliberate dynamic/private policy
/downloads/... → explicit signed-access and origin policy
```

Inspect Cache-Control, selected cache key, forwarded cookies/query values, and origin logs. A CDN is another copy with a freshness contract, not a replacement for Rails authorization.''',
 '''Browser request → edge key lookup → cached response or origin fetch → response headers → app behavior. Trace a permission change and decide whether an already cached/signed response remains usable.

For deployment, keep the HTML shell and referenced asset versions compatible. A stale shell pointing to removed files can break the app even when the new bundle is correct.''',
 'Caching personalized JSON under one shared key is dangerous. Removing old assets immediately can break clients with cached HTML. An invalidation is not a substitute for a correct cache policy.',
 'User A’s ticket list appears for user B after enabling CDN caching. Repair the cache contract.',
 'Disable unsafe shared caching for that private path or use an authorization-aware policy with a correctly scoped cache identity. Verify origin access and user separation. Test two distinct accounts and revocation, not only speed.',
 'A release removes old hashed JS files while some browsers retain old HTML. What should change?',
 'Retain compatible old assets for a deliberate window and manage HTML freshness separately. Use content-addressed asset names and test rolling release/cache overlap. Do not assume every browser fetches the latest shell immediately.',
 [q('What defines which requests can share a cached response?','The cache key/policy','Only the origin URL name','The Rails class name',0,'Identity and forwarded dimensions must match response variation.'),q('Should personalized JSON be shared blindly?','Yes','No','Only if gzipped',1,'Cache scope is an access boundary.'),q('Why retain old versioned assets temporarily?','Cached HTML may still reference them','They improve SQL plans','To avoid authorization',0,'Clients can remain on older shell versions.')],
 'A cache key is a sharing decision.', ['Request identity','Edge cache key','Hit or allowed origin','Freshness and access','Compatible assets'], [('CloudFront guide',AWS+'AmazonCloudFront/latest/DeveloperGuide/Introduction.html')],usecase='Vue assets and controlled download delivery.',benefits='Lower origin load and faster geographically distributed reads.',drawbacks='Cache identity, invalidation, and asset compatibility add correctness work.',tags=['aws','cdn','frontend'])

chapter('cloud','rds','RDS PostgreSQL: managed database, owned data model','intermediate',
 'Configure private connectivity, backups, failover expectations, and Rails connection limits.',
 '''RDS manages parts of database infrastructure, not your schema, query design, or business rules. You still choose engine/version, instance/storage settings, network, credentials, backup retention, maintenance, and application connection behavior.

High availability and read scaling are different goals. A standby/failover arrangement is not automatically the same thing as an application read replica. Read replicas can lag; sending a read-after-write there can show old data. Use the selected RDS deployment type’s exact contract.

Setup: choose a training PostgreSQL engine/version, private subnet group and DB security group, credential delivery, backup/restore policy, connection settings, and monitoring. Test connection failure and a restore to a separate instance with synthetic data. A backup checkbox is not a completed recovery exercise.''',
 '''```yaml
# Rails database.yml concept; values arrive from the training environment.
production:
  adapter: postgresql
  host: <%= ENV.fetch('DB_HOST') %>
  database: <%= ENV.fetch('DB_NAME') %>
  username: <%= ENV.fetch('DB_USER') %>
  password: <%= ENV.fetch('DB_PASSWORD') %>
  pool: <%= ENV.fetch('DB_POOL', '5') %>
```

Configure TLS/certificate verification according to your pg/client and RDS setup. Do not log the rendered connection credentials.''',
 '''Rails checks out a connection → network/TLS/authentication → SQL/locks → commit → connection returns to pool. Multiply pool size by web/worker process count before comparing with DB limits.

During failover, existing connections can break. The app needs bounded retry/reconnect behavior and must not retry a non-idempotent transaction blindly after an unknown commit outcome.''',
 'Managed backups do not prove your restore time. More app replicas can multiply connections. Read-replica lag can look like a lost update to the user.',
 'Scaling workers from 2 to 20 exhausts DB connections. What capacity calculation was missing?',
 'Count processes and per-process pool limits across web, workers, migrations, and admin use. Measure active/waiting connections and transaction duration. Bound concurrency/pools and shorten held transactions before increasing limits indiscriminately.',
 'The user saves a ticket then reads stale data from a replica. How can the product meet a read-your-write expectation?',
 'Route the relevant read to the authoritative writer or use a deliberate consistency/lag-aware strategy. Do not claim that any read replica is instantly current. Test failover and stale-read behavior with the chosen deployment type.',
 [q('Does RDS design your indexes?','Yes','No','Only for Rails',1,'Application query/schema decisions remain yours.'),q('What can read replicas introduce?','Replication lag','Guaranteed immediate read-your-write','Automatic business authorization',0,'Read scaling and consistency are separate choices.'),q('What proves recovery capability best?','A measured restore exercise','A backup setting alone','A green web icon',0,'You need evidence the data can be restored and used.')],
 'Managed infrastructure does not remove application data responsibility.', ['Private DB access','Bounded connection pool','SQL and constraints','Backup/failover path','Measured recovery'], [('RDS overview',AWS+'AmazonRDS/latest/UserGuide/Welcome.html')],usecase='The Rails source-of-truth database.',benefits='Managed infrastructure tasks and supported backup/HA features.',drawbacks='Queries, pool limits, restore evidence, and consistency remain your work.',tags=['aws','rds','postgresql'])

chapter('cloud','elasticache','ElastiCache: choose managed cache and queue roles deliberately','intermediate',
 'Separate cache data from durable work and plan client behavior during eviction or failover.',
 '''ElastiCache supplies managed in-memory engines/options. Identify the selected engine and mode rather than assuming every Redis-compatible feature and durability behavior is identical. Client compatibility, topology, authentication, TLS, and failover matter.

A disposable cache can evict/rebuild data. A background queue’s work may not be safely disposable. Mixing both under one eviction and memory policy can turn a cache-pressure event into lost jobs. Isolate roles according to their correctness needs.

Setup: choose engine/mode, private connectivity, access/TLS settings, memory/eviction policy, client timeout/pool behavior, and monitoring. Test a cold cache, memory pressure, and endpoint/failover changes with synthetic data. Do not expose a cache endpoint publicly to avoid a VPC configuration problem.''',
 '''```text
Rails read cache → rebuildable ticket summaries, bounded TTL
Background-job Redis → deliberate job durability/memory policy
Session store → explicit loss and logout behavior
```

Different roles may need separate instances or clusters. A shared endpoint is not free simply because the client library looks the same.''',
 '''Cache miss → authoritative DB read → cached copy → later hit → expiry/eviction → rebuild. Then trace failover: client connection breaks, DNS/topology changes, operations retry under the selected contract.

Monitor memory, eviction, latency, connection count, and application fallback load. A cache outage can overload PostgreSQL if every request immediately falls back.''',
 'A cache is not permission authority. A Redis queue on an eviction-enabled shared cache can lose work. A cold-cache stampede can create a database incident.',
 'A memory-pressure event evicts job keys and ticket-cache keys together. Repair the role separation.',
 'Isolate durable-work and disposable-cache roles with suitable memory/eviction/durability settings. Verify client behavior and recovery for the queue. Cache data can be rebuilt; missing business work needs reconciliation from a durable source.',
 'A failover causes a surge of database queries. What should the cache-fallback design include?',
 'Bound concurrent rebuilds, use jittered TTLs and appropriate request coalescing, and monitor fallback load. Define stale-serving limits where allowed. Do not make a cache failure turn into unlimited DB work.',
 [q('Are cache entries and queued work equally disposable?','Always','No','Only when both use strings',1,'Their correctness and recovery requirements differ.'),q('What can a cold cache cause?','A surge at the source database','Guaranteed lower load','Immediate data correctness proof',0,'Misses can synchronize into a stampede.'),q('What should engine selection record?','Actual engine/mode and supported client contract','Only the Redis logo','Only region',0,'Managed options do not all have identical behavior.')],
 'Same protocol does not mean the same data responsibility.', ['Choose data role','Private managed endpoint','Client and memory policy','Miss or failover','Bounded rebuild/recovery'], [('ElastiCache overview',AWS+'AmazonElastiCache/latest/dg/WhatIs.html'),('Redis eviction','https://redis.io/docs/latest/develop/reference/eviction/')],usecase='Rails caches, sessions, and queue infrastructure.',benefits='Managed in-memory service operations.',drawbacks='Role mixing and fallback behavior can threaten correctness or the DB.',tags=['aws','redis','cache'])

chapter('cloud','sqs','SQS: work delivery, visibility, and deletion','intermediate',
 'Set up a queue and dead-letter path and implement repeat-safe processing.',
 '''A queue hands work to consumers. Receiving an SQS message does not remove it; visibility temporarily hides it under the queue’s contract. Successful processing is followed by deliberate deletion using the receipt handle. If processing fails or times out, work can be seen again.

Standard and FIFO queues have different ordering/deduplication options, but neither makes your external side effect universally exactly once. A worker can commit to PostgreSQL and crash before deletion. Design the business effect to handle repetition.

Setup: choose queue type from the required ordering/throughput semantics, configure visibility/retention, a DLQ redrive policy, narrow producer/consumer permissions, and long polling. Test duplicate delivery, a poison message, and a job longer than the visibility window.''',
 '''```ruby
require 'aws-sdk-sqs'
sqs = Aws::SQS::Client.new(region: ENV.fetch('AWS_REGION'))
messages = sqs.receive_message(queue_url: ENV.fetch('QUEUE_URL'),
  wait_time_seconds: 20, max_number_of_messages: 10).messages
messages.each do |message|
  process_idempotently(message.body) # commit durable effect first
  sqs.delete_message(queue_url: ENV.fetch('QUEUE_URL'),
    receipt_handle: message.receipt_handle)
end
```

The loop is a teaching boundary. Add graceful shutdown, bounded concurrency, validation, visibility extension, error policy, and telemetry for a real worker.''',
 '''Send → visible → receive → temporarily invisible → DB effect → delete. Crash after DB commit but before delete leads to repetition, which a unique event/command identity must tolerate.

DLQ means quarantined for investigation, not successfully processed. Redrive after a repair needs a repeat-safe consumer and an understanding of ordering consequences.''',
 'Deleting before processing can lose work. A too-short visibility window can overlap processing. A long visibility value can delay recovery after a real crash.',
 'A report worker takes 90 seconds but visibility is 30 seconds and two workers generate duplicate output. Repair it.',
 'Choose/extend visibility for the actual processing window, bound work, and enforce a unique logical report run. Delete only after durable completion. Test crash after effect before delete; visibility alone is not deduplication.',
 'A message repeatedly fails JSON validation. What is the recovery path?',
 'Record a safe diagnostic, quarantine after a deliberate attempt policy, alert on age/count, repair the producer/schema or consumer, then redrive deliberately. Avoid infinite tight retries and do not silently delete required work.',
 [q('Receiving an SQS message immediately deletes it?','Yes','No','Only with long polling',1,'Receipt and deletion are distinct operations.'),q('What handles crash after DB commit before delete?','Idempotent business processing','Only a bigger visibility timeout','Only gzip',0,'The message can be delivered again.'),q('What does a DLQ indicate?','Work needs investigation/recovery','All work succeeded','The DB transaction rolled back automatically',0,'Quarantine is an operational state, not success.')],
 'Receive. Do durable work. Delete. Expect repeats.', ['Queue message','Visibility window','Repeat-safe DB effect','Delete receipt handle','DLQ or recovery'], [('SQS visibility',AWS+'AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html')],usecase='Exports and independent background tasks.',benefits='Managed work delivery and buffering.',drawbacks='Visibility, duplicate effects, and DLQ recovery still need design.',tags=['aws','sqs','messaging'],lab='aws-rails')

chapter('cloud','sns','SNS: fan out one fact to independent subscribers','beginner',
 'Distinguish publish/subscribe fan-out from competing workers on a queue.',
 '''SNS can publish a message to subscriptions. This is fan-out: independent destinations can receive the same published fact. A set of workers competing on one queue instead shares work among them. Choose based on whether each downstream system needs its own copy.

Use SNS-to-SQS when subscribers need their own buffering and processing pace. Define message schema, subscription filtering, access policies, and failure/retry handling. Delivery behavior depends on topic and subscription types; record the exact option rather than assuming one global ordering guarantee.

Setup: create a training topic, create a separate queue for each durable subscriber role, add subscriptions/filters, allow only the intended topic to send to each queue, then publish a synthetic event and verify each required subscriber independently.''',
 '''```text
TicketCompleted topic
  → reporting queue → reporting workers
  → notification queue → notification workers
```

Three reporting workers on the reporting queue share reporting work. They are not three separate business subscriptions.''',
 '''Publisher sends one fact → SNS evaluates subscriptions/filters → each destination receives according to its delivery contract → each queue/consumer manages its own completion. One slow subscriber should not dictate another’s progress when their buffers are separate.

Carry an event ID for duplicate handling and traceability. A publish acknowledgement does not prove every subscriber’s business effect completed.''',
 'Putting all independent subscribers on one queue makes them compete for messages instead of each receiving all required facts. An overly broad queue policy can allow unintended senders.',
 'Reporting and notification workers read one queue, so some tickets get only reporting and some only notifications. Repair the topology.',
 'Give each independent subscriber a queue and fan out the event to both, with explicit policies and schema. Keep competing workers only within the same subscriber role. Test that one event reaches both logical consumers.',
 'A new subscriber is added months later and needs historical events. Is a live fan-out topic alone enough?',
 'Check the chosen retention/replay contract and provide an archive/backfill source if needed. A simple live fan-out design is not automatically a replayable historical log. This requirement may favor Kafka or a deliberate archive pipeline.',
 [q('What is fan-out?','Independent subscribers receive the fact','Workers always divide one copy','A database join',0,'Each logical subscriber has its own work to do.'),q('One queue shared by unrelated consumers creates what risk?','They compete instead of each seeing every event','Every event is automatically broadcast','No buffering',0,'Queue worker groups usually share work.'),q('Publish acknowledgement proves every business effect?','Yes','No','Only with JSON',1,'Transport acceptance and downstream completion differ.')],
 'One queue shares work. Fan-out copies responsibility.', ['Published fact','Topic subscriptions','Independent queues','Competing workers per role','Separate completion'], [('SNS overview',AWS+'sns/latest/dg/welcome.html')],usecase='A ticket event consumed by reporting and notifications.',benefits='Simple fan-out with independently buffered subscribers.',drawbacks='Schema, delivery type, policies, and history/backfill remain explicit choices.',tags=['aws','sns','messaging'])

chapter('cloud','eventbridge','EventBridge: route integration events by meaning','intermediate',
 'Configure an explicit event bus/rule/target contract and debug a missing delivery.',
 '''EventBridge connects event sources and targets with routing/filtering features. It is useful when you integrate AWS/service events or route application facts by a structured envelope. Choose the actual bus/pipe offering and its documented retention/ordering/replay behavior; newer offerings can differ from classic rule-based examples.

This chapter’s setup uses a deliberate classic-style custom bus, event pattern, and target such as SQS. An event pattern selects meaning from fields such as source and detail-type. It does not validate every business rule inside detail.

Setup: choose the supported bus type, define a small event schema, create a matching rule and target permission, configure delivery failure handling, and send one matching and one non-matching event. Inspect the producer response for per-entry failure rather than treating the HTTP request alone as success.''',
 '''```json
{"source":["learning.tickets"],"detail-type":["TicketCompleted"]}
```

The rule targets a reporting queue under an explicit policy. Include event_id, workspace_id, ticket_id, schema_version, and occurred_at in a minimal detail envelope. Do not publish whole private model snapshots.''',
 '''Application emits structured entry → event service accepts/rejects that entry → pattern matches → permitted target receives → consumer handles business effect. Debug one hop at a time with event/request identity.

If no target event appears, check producer entry result, bus/region/account, pattern field spelling/type, target permission, delivery retry/DLQ state, and consumer state.''',
 'A successful batch API call can include failed entries. A pattern mismatch is different from a consumer crash. Bus products and ordering/replay features must not be generalized from an old diagram.',
 'The API returns success but one of ten events never reaches the target. What do you inspect?',
 'Check per-entry results first, then bus context, pattern match, target permission, delivery failures, and downstream receipt. Retain logical event identity for safe retry of only failed entries.',
 'A business workflow requires ordered replay over months. What must you verify before selecting this route?',
 'Verify the chosen offering’s exact ordering, retention, replay, throughput, and consumer-state contract. Compare it with a retained Kafka log and the team’s needs. Do not assume either product name supplies all guarantees.',
 [q('Does one successful batch HTTP call prove every entry succeeded?','Yes','No','Only with a rule',1,'Inspect per-entry outcomes.'),q('What does a routing pattern primarily select?','Events matching field conditions','Valid database transactions','Completed user workflows',0,'Routing is not full business validation.'),q('Which context can explain a missing event?','Wrong bus, account, region, or target permission','Only button color','Only the Ruby class name',0,'Trace the integration boundary systematically.')],
 'Accepted entry → matched rule → delivered target → completed effect.', ['Structured event','Entry acceptance','Selected bus and pattern','Permitted target','Consumer outcome'], [('EventBridge overview',AWS+'eventbridge/latest/userguide/eb-what-is.html')],usecase='AWS integrations and structured application-event routing.',benefits='Managed routing/filtering and service integration.',drawbacks='Offering-specific contracts, per-entry failures, and target policies need attention.',tags=['aws','eventbridge','messaging'])

chapter('cloud','lambda','Lambda event functions: small work with explicit retry boundaries','beginner',
 'Choose an event-function boundary and handle retry, concurrency, and database pressure.',
 '''This chapter focuses on Lambda event functions: a handler invoked under a configured event source. Other Lambda offerings have different contracts. A small S3 metadata check or queue-driven transformation can fit well; a large always-warm Rails web process is a different decision.

The trigger controls invocation and retry semantics. A queue event source is not identical to a synchronous API call. A batch can contain several records, and reporting failure incorrectly can repeat already completed items. Keep the logical effect idempotent.

Setup: choose the runtime and handler, attach a narrow execution role, configure environment/secret access, timeout/memory/concurrency, connect the event source, and test failure plus repeated delivery. If using private database access, plan network paths and connection multiplication.''',
 '''```ruby
# Handler shape illustration for a selected Ruby event runtime.
def handler(event:, context:)
  event.fetch('Records').each do |record|
    handle_record_idempotently(record)
  end
  { processed: event.fetch('Records').length }
end
```

The event schema and partial-batch response must match the selected trigger. Do not copy this return value as if it acknowledges every source type correctly.''',
 '''Source event → invocation/batch → validate record → durable effect → source-specific acknowledgement/failure handling. A retry may invoke the handler again with the same logical item.

Measure cold-start and dependency latency for the actual interaction. Bound concurrency so a surge does not create more database connections than RDS can support.''',
 'Stateless compute does not mean the business effect is idempotent. Execution environments may be reused, so avoid treating mutable globals as per-user durable state.',
 'A queue batch contains ten records; one fails and the whole batch is retried, duplicating nine effects. Improve the contract.',
 'Make each effect idempotent and use the source’s supported partial-batch failure contract when appropriate. Record per-record identity/results. Test a crash after one successful effect and before acknowledgement.',
 'A concurrency surge overwhelms PostgreSQL. What should be bounded?',
 'Invocation concurrency, per-invocation connection use, and transaction duration. Consider a supported connection-management approach and queue buffering. More automatic compute scaling is not automatic downstream capacity.',
 [q('Does each trigger have identical retry behavior?','Yes','No','Only in Ruby',1,'Invocation/acknowledgement semantics depend on the event source.'),q('What can unbounded function concurrency overload?','A fixed-capacity database','Only the browser','Nothing, because serverless',0,'Downstream systems still have limits.'),q('Should a generic handler return be copied to every event source?','Yes','No','Only with JSON',1,'Batch acknowledgement contracts differ.')],
 'Small handler, explicit source contract, bounded downstream work.', ['Configured source','Invocation identity','Repeat-safe handler','Source acknowledgement','Concurrency and error metrics'], [('Lambda overview',AWS+'lambda/latest/dg/welcome.html')],usecase='Queue/S3-triggered small processing steps.',benefits='Managed event-driven compute without operating a VM per handler.',drawbacks='Trigger semantics, cold starts, concurrency, and downstream limits remain.',tags=['aws','lambda','events'])

chapter('cloud','ecr','ECR: publish an artifact you can identify and replace','beginner',
 'Explain image tags, digests, registry access, scan results, and release retention.',
 '''A container registry stores images. A tag is a name that can move unless policy prevents it. A digest identifies image content. Deploying latest makes it difficult to know what actually ran during an incident.

ECR integrates registry access with AWS identity. Build/push identity and workload pull identity can have different permissions. A successful push does not prove the image runs, and a vulnerability scan does not prove the application is safe or compatible.

Setup: create a deliberate training repository, configure tag policy/retention, authenticate the build identity, build from an identified source revision, push a revision tag, record the digest, and test pull/run under the workload’s identity. Keep rollback artifacts long enough for the release plan.''',
 '''```text
Source commit → reproducible image build → ECR repository
Tag: git-<revision>
Digest: sha256:<content identity>
Deployment: repository@sha256:<verified digest>
```

CLI login/push commands belong in a controlled pipeline or chosen training session. No registry upload is performed by the course application.''',
 '''Build → scan/check → push → resolve digest → deploy that artifact → observe → roll back to a known digest if needed. Connect logs/deployment metadata to the source and digest.

Retention rules must not remove every artifact needed for rollback. Large layers and old tags also consume storage; define a deliberate policy.''',
 'latest can mean different images on two machines. Credentials copied into a Docker layer remain in the image even if a later command removes the file.',
 'Two replicas pull latest at different times and run different code. Repair release identity.',
 'Build once, record a verified digest, and deploy that same immutable artifact to every intended replica. Keep source provenance and rollback digest. Do not rebuild the same release label from an uncommitted tree.',
 'A registry scan is clean. What still needs verification?',
 'Application behavior, configuration, permissions, runtime dependencies, and the relevant failure paths. Scanning is one input to release risk, not a complete correctness/security proof.',
 [q('Which is content identity?','Image digest','A mutable latest tag','A branch nickname',0,'A digest identifies the image bytes.'),q('Does push success prove runtime success?','Yes','No','Only on ECS',1,'Run and configuration checks are separate.'),q('What should retention consider?','Rollback artifacts as well as storage cost','Only deleting everything old','Only the newest tag',0,'A lifecycle policy must preserve the recovery plan.')],
 'Build once. Name the bytes. Deploy those bytes.', ['Source revision','Image build','Registry digest','Workload pull','Observed release identity'], [('ECR guide',AWS+'AmazonECR/latest/userguide/what-is-ecr.html')],usecase='Rails/Vue container delivery.',benefits='Managed artifact distribution and AWS access integration.',drawbacks='Mutable tags, retention, and image-layer hygiene need policy.',tags=['aws','ecr','delivery'])

chapter('cloud','ecs','ECS with Fargate: web and workers as separate services','intermediate',
 'Configure task definitions, roles, networking, logs, health, and scaling for Rails web and worker processes.',
 '''ECS orchestrates tasks and services. A task definition describes containers, resources, ports, configuration, and roles. A service maintains a desired task count. Fargate is a capacity option that removes much of the host management; it does not remove application or network responsibility.

Use the same image with different process commands for web and workers when that fits the app. Scale them from their own signals: request pressure for web, backlog/age and safe concurrency for workers. A DB migration is a deliberate one-off task, not an action every new replica should race to run.

Setup: push an image to ECR, create execution/task roles, define task resources and commands, choose private networking/egress, wire logs and secrets, attach web targets to ALB, configure health/graceful shutdown, then run a smoke path and a worker failure.''',
 '''```text
Task definition tickets-web: image@digest, command bundle exec puma
Task definition tickets-worker: same image, deliberate worker command
Web service → ALB target group
Worker service → queue and DB permissions
One-off release task → compatible migration
```

Do not copy a web health probe onto a worker that does not run HTTP. Define worker health from progress and process behavior.''',
 '''Scheduler starts task → platform pulls image using execution role → app receives workload task role/config → process becomes ready → traffic/work arrives → logs/metrics report progress. On shutdown, stop accepting new work and finish or safely retry current work.

Count DB pools across every web and worker task before scaling. Managed task placement does not expand PostgreSQL capacity.''',
 'An execution role is not automatically the app’s S3 role. Starting more workers can overload the DB/provider. A task repeatedly failing before logs are configured is hard to diagnose.',
 'The app starts but S3 access fails while image pull succeeds. What role distinction matters?',
 'Image/platform operations may use the execution role; app AWS calls use the task role. Verify the effective app identity and its scoped permission. Also check private network paths and resource policies.',
 'A queue backlog grows. Should worker count double immediately?',
 'Measure processing rate, oldest age, error/retry rate, DB pool pressure, and provider limits. Scale within downstream capacity and fix poison/slow work. A larger worker count can worsen the bottleneck.',
 [q('What maintains a desired long-running task count?','An ECS service','Only an image tag','A SQL migration',0,'The service reconciles running tasks.'),q('Fargate removes which concern?','Much host management, not app responsibility','Every networking setting','All database limits',0,'Managed capacity still needs application design.'),q('Where should migrations usually run?','A deliberate release/one-off task','Every request','Every new replica without coordination',0,'Schema changes need controlled ownership.')],
 'Image, command, role, network, health, and desired count.', ['Task definition','Image and platform role','Application task role','Web or worker service','Health and bounded scaling'], [('ECS guide',AWS+'AmazonECS/latest/developerguide/Welcome.html')],usecase='A containerized Rails app without a Kubernetes requirement.',benefits='Managed orchestration with direct AWS integration.',drawbacks='Networking, release flow, identity, and capacity limits remain explicit.',tags=['aws','ecs','fargate'])

chapter('cloud','eks','EKS: Kubernetes control plane does not operate your application','intermediate',
 'Choose EKS for a concrete Kubernetes need and map AWS responsibility versus cluster/workload responsibility.',
 '''EKS supplies managed Kubernetes offerings. You still need to understand the selected mode’s responsibilities: workload configuration, identity, networking, storage, admission/access, observability, upgrades, and application recovery.

Choose Kubernetes when its APIs/ecosystem and team needs justify the operational surface. A small Rails web/worker service may fit ECS more simply. EKS is not the required next level after learning Docker; it is a different operating model.

Setup outline: choose the supported cluster/mode/version, establish access and workload identity, network/node or managed-capacity settings, registry/logging, ingress/load balancing, secrets delivery, and resource/probe policies. Deploy a training namespace and verify one request and one rescheduled pod before adding more tools.''',
 '''```text
AWS: chosen EKS control-plane/capacity integration contract
Kubernetes: Deployment → ReplicaSet → Pods
Service/Ingress integration → AWS load balancer path
Pod identity → allowed AWS calls
Rails → DB constraints, transactions, and app behavior
```

The Kubernetes chapters supply local manifests. They are not an automatic EKS provisioning script.''',
 '''Manifest desired state → API admission → controller reconciliation → scheduler/capacity → pod process → readiness → service traffic. Then trace a pod reschedule and a rollout with the DB unchanged.

Map every secret, network permission, and persistent data store to its owner. A healthy control plane does not prove your app is healthy.''',
 'Running a DB in a StatefulSet does not create a complete backup/HA plan. A broad node role can accidentally become every pod’s effective access. More platform components can increase incident surface.',
 'A team selects EKS only because “industry uses Kubernetes.” Write the decision comparison.',
 'Compare required portability/API ecosystem, team skills, operational ownership, workload complexity, and AWS integration against ECS or simpler compute. Choose EKS for a specific benefit and budget its lifecycle work.',
 'The cluster is healthy but users get 503s after a deployment. Where do you look?',
 'Inspect pod events/logs, readiness, Service selectors/endpoints, ingress/load balancer target health, and app dependencies. Control-plane health is a different signal from workload readiness.',
 [q('Does a healthy EKS cluster prove Rails is ready?','Yes','No','Only with two nodes',1,'Workload and control-plane health are separate.'),q('Is Kubernetes mandatory after Docker?','Yes','No','Only for Ruby',1,'Choose orchestration from actual needs.'),q('What should pod AWS access use?','A deliberate supported workload identity','A universal broad node identity by habit','A committed access key',0,'Workload permissions should be scoped intentionally.')],
 'Managed control plane. Deliberately operated workload.', ['EKS responsibility map','Kubernetes desired state','Pod identity and network','Readiness and ingress','Observed app behavior'], [('EKS overview',AWS+'eks/latest/userguide/what-is-eks.html')],usecase='Teams with a justified Kubernetes platform need.',benefits='Managed Kubernetes integration and ecosystem access.',drawbacks='Workload/platform lifecycle remains substantial.',tags=['aws','eks','kubernetes'])

chapter('cloud','msk','MSK: managed Kafka still needs event design','intermediate',
 'Map broker management, clients, network, identity, partitions, and consumer operations in AWS.',
 '''MSK provides managed Kafka options. It reduces parts of broker infrastructure work, but does not choose event keys, schemas, consumer groups, offset policy, or business idempotence for you. Provisioned/serverless options have different configuration and capacity contracts.

A client needs reachable advertised broker endpoints, the selected authentication/TLS mechanism, authorization, and compatible client support. “The bootstrap server responds” is not enough if metadata returns endpoints the client cannot reach.

Setup: choose the MSK offering/version, private connectivity and access mechanism, topic/partition policy, client credentials/role support, monitoring, and retention. Run the local Kafka lab first. Then test a synthetic event and replay in the chosen training AWS environment.''',
 '''```text
Rails outbox → producer adapter → reachable MSK brokers
Topic key = ticket identity
Reporting group → repeat-safe PostgreSQL projection
Metrics = producer errors, consumer lag/age, processing errors, retention headroom
```

The local PLAINTEXT development listener is not the cloud security configuration. Choose authentication and client settings from the selected MSK mode’s docs.''',
 '''Client contacts bootstrap → discovers leaders → authenticates/connects to actual brokers → produces keyed record → group consumes/commits under its own policy. Debug network, auth, topic access, and business processing separately.

Retention and consumer downtime interact. A lagging consumer can lose required history after retention; managed brokers do not extend the business recovery window automatically.''',
 'MSK does not make a Rails DB write and Kafka publish atomic. Client libraries can require explicit support for the selected authentication method. A topic with one hot key can bottleneck despite more brokers.',
 'A producer reaches bootstrap but fails after metadata lookup. What is a likely class of problem?',
 'Inspect advertised broker endpoints and actual client reachability/DNS/TLS/auth for those endpoints. Bootstrap is discovery, not a permanent proxy for all traffic. Keep request/error identities and avoid exposing brokers to bypass network design.',
 'A consumer was down longer than retention. What must the recovery plan provide?',
 'An authoritative rebuild/backfill source or suitable archive/retention design. Resetting offsets cannot recover records that are no longer retained. Verify the exact recovery window and data policy.',
 [q('Does managed Kafka solve the DB/publish dual-write gap?','Yes','No','Only in AWS',1,'The application still needs an outbox or another explicit consistency design.'),q('Bootstrap is primarily what?','Discovery of cluster metadata','A universal proxy for every record','A database transaction coordinator',0,'Clients connect to relevant broker endpoints.'),q('Can offset reset restore expired records?','Yes','No','Only to earliest',1,'Offsets cannot recreate deleted history.')],
 'Managed brokers, still your event contract.', ['Client network and identity','Broker metadata','Keyed topic','Consumer group','Lag and recovery window'], [('MSK overview',AWS+'msk/latest/developerguide/what-is-msk.html')],usecase='The local Rails/Kafka design moved to a managed AWS environment.',benefits='Managed broker infrastructure choices.',drawbacks='Client integration, business correctness, and recovery remain yours.',tags=['aws','msk','kafka'])

chapter('cloud','cloudwatch','CloudWatch: logs, metrics, alarms, and a useful runbook','beginner',
 'Connect an application symptom to a metric, trace/log identity, alarm, and recovery check.',
 '''Logs explain individual events. Metrics summarize trends. Traces connect steps across boundaries. CloudWatch provides AWS-native observability capabilities; choose the signals and retention you actually need.

An alarm should point to user impact or a meaningful precursor, not merely an interesting chart. “Oldest export age is growing” can be more actionable than queue count alone. Include scope, threshold/time window, owner, and the first safe checks.

Setup: send structured app/container logs, define bounded metric dimensions, retain data deliberately, add a small dashboard and alarm, then simulate a synthetic failure and follow the runbook. Do not emit user IDs or event IDs as unbounded metric labels.''',
 '''```json
{"event":"receipt_attempt","event_id":"synthetic-e1","attempt":2,
 "outcome":"timeout","duration_ms":850,"request_id":"synthetic-r1"}
```

Use event/request IDs in controlled logs/traces for correlation. Metrics might use bounded service, environment, and outcome categories. Avoid logging payloads or secrets.''',
 '''User reports delay → check success/latency and oldest pending age → inspect correlated logs/trace → identify provider, DB, or consumer boundary → apply safe repair → verify backlog drains and user outcome recovers.

Test the alert path itself. A dashboard nobody watches does not wake an owner during a serious incident.''',
 'High-cardinality metric dimensions can increase cost and reduce usability. An alert without a runbook can become noise. A green process metric can coexist with no business progress.',
 'Every ticket ID becomes a metric dimension and costs rise. Repair the signal design.',
 'Use bounded aggregate dimensions for metrics and put per-ticket correlation in appropriately protected logs/traces. Review retention and sampling. Keep a metric for user-visible success/backlog age and a runbook for failures.',
 'The queue count is stable but oldest age keeps growing. What does that suggest?',
 'Some work may be stuck or repeatedly failing while newer work completes. Inspect age distribution, poison items, retries, and per-consumer progress rather than assuming stable count means healthy processing.',
 [q('Which signal summarizes trends?','Metrics','Only a single stack trace','A secret file',0,'Metrics aggregate behavior over time.'),q('Where do high-cardinality event IDs usually belong?','Correlated logs/traces rather than ordinary metric labels','Every metric dimension','Only CSS attributes',0,'Metric dimensions should be deliberately bounded.'),q('A useful alarm includes what?','Owner and first checks/recovery verification','Only a red color','Only the service logo',0,'An alarm should lead to action.')],
 'Signal → question → safe action → verified recovery.', ['Structured signals','Bounded metrics','Actionable alarm','Correlation and diagnosis','Recovery evidence'], [('CloudWatch overview',AWS+'AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html')],usecase='Rails API and worker operations.',benefits='AWS-native signal collection and alerting.',drawbacks='Signal volume, cardinality, retention, and alert noise need design.',tags=['aws','observability'])

chapter('cloud','secrets-kms','Secrets Manager and KMS: credentials and encryption keys are different','intermediate',
 'Deliver secrets and authorize key use without confusing encryption with application access.',
 '''A secret is a value the app needs, such as a database password. An encryption key protects cryptographic operations/data under a key policy. Secrets Manager and KMS address related but different responsibilities.

Use workload identity to retrieve an allowed secret or use a key. Encryption at rest does not prove that the application is allowed to show a record to this user. Secret rotation also needs client behavior: a long-lived connection/client may keep using an old value until refreshed or reconnected.

Setup: create a training secret, choose its key policy, grant narrow workload retrieval/decryption access as required, choose injection versus runtime retrieval/cache, and test rotation/failure. Keep secret values out of source, image layers, logs, screenshots, and AI context.''',
 '''```ruby
require 'aws-sdk-secretsmanager'
client = Aws::SecretsManager::Client.new(region: ENV.fetch('AWS_REGION'))
response = client.get_secret_value(secret_id: ENV.fetch('DB_SECRET_ID'))
config = JSON.parse(response.secret_string)
# Validate expected fields. Never print config.
```

Retrieving on every request is usually unnecessary. Cache/refresh under a deliberate lifetime and failure policy; account for workload restarts when secrets are injected only at startup.''',
 '''Workload role → permitted secret retrieval/key use → validated runtime config → client connection → rotation → refresh/reconnect. Test denied access and stale credentials without revealing values.

For incident response, distinguish revoking application access, rotating a credential, and changing encryption-key policy. They do not all revoke an already issued download URL or terminate every connection instantly.''',
 'Encrypting a secret in Git does not automatically establish safe key ownership. A successful secret fetch does not prove the DB accepts it. Rotation without refresh can cause intermittent failures.',
 'A secret rotates, but old workers keep failing authentication while new workers succeed. Explain the lifetime mismatch.',
 'Old processes may retain injected/cached values or connections. Define refresh/restart/reconnect behavior, overlap, and error handling. Test rotation with both old and new processes. Do not log the values to compare them.',
 'All objects are encrypted, but a user can download another tenant’s object. What boundary is still broken?',
 'Application/resource authorization and key selection may be wrong. Encryption at rest protects a storage threat boundary, not every caller access decision. Resolve keys from authorized records and scope workload permissions.',
 [q('Is a database password the same thing as a KMS key?','Yes','No','Only in Rails',1,'Secrets and cryptographic keys have different lifecycles and APIs.'),q('Does encryption at rest prove tenant access correctness?','Yes','No','Only with a managed service',1,'Authorization is a separate rule.'),q('What must rotation account for?','Client/cache/connection lifetime','Only the new secret value','Only a dashboard label',0,'Processes may keep old values or connections.')],
 'Secret value, key permission, client lifetime, user permission.', ['Workload identity','Secret/key permission','Validated config','Client lifetime','Rotation and access test'], [('Secrets Manager',AWS+'secretsmanager/latest/userguide/intro.html'),('KMS concepts',AWS+'kms/latest/developerguide/concepts.html')],usecase='Database credentials and private object encryption.',benefits='Central secret/key lifecycle and access control.',drawbacks='Rotation, caching, and multiple policy layers need operational tests.',tags=['aws','secrets','kms'])

chapter('cloud','architecture','A complete Rails application on AWS: trace four journeys','intermediate',
 'Explain the request, attachment, background job, and event paths, including cost and recovery choices.',
 '''Use a modular Rails app with web and workers, PostgreSQL as the business source, private attachments, a cache, and deliberate event delivery. Choose ECS/Fargate as one baseline; EKS is an alternative when Kubernetes benefits justify it. They are not two layers every app must run together.

Trace four journeys: a user opens a ticket, uploads an attachment, requests a report, and completes a ticket that updates reporting. For each, name identity, network, authoritative write, asynchronous boundary, user-visible state, and recovery path.

Then stress the design: one zone fails, the provider slows, a worker repeats, the DB pool fills, a secret rotates, or a user loses access. Cost reasoning includes always-on capacity, storage/retention, data transfer, NAT/endpoints, logs, and managed service overhead. Use current regional pricing when actually provisioning; this course does not promise a free deployment.''',
 '''```text
Route 53 + ACM → ALB → Rails web (ECS or EKS)
                           → RDS PostgreSQL
                           → ElastiCache for a defined cache role
Browser ↔ authorized S3 upload/download; CloudFront for deliberate delivery
Rails outbox → dispatcher → MSK/Kafka → reporting consumer → projection
Report request → SQS/worker → S3 result
All paths → request/event identity → CloudWatch/Datadog telemetry
Workload roles + Secrets Manager/KMS across explicit boundaries
```

Draw ECS and EKS as alternatives in your decision sketch, not a mandatory chain.''',
 '''For each journey, point to where success is durable. A report request is not a ready file. An outbox commit is not a consumed event. A cache hit is not a new permission grant.

Write one runbook for a growing report age and one restore rehearsal for PostgreSQL/object metadata. Define RPO (acceptable data loss window) and RTO (acceptable recovery time) in plain task terms.''',
 'Putting every named tool into one diagram can create needless operational burden. HA without restore/reconciliation evidence is incomplete. A rollback cannot unsend notifications or restore all deleted data.',
 'The team adds Kafka, Cassandra, EKS, and Redis to a small ticket app without a requirement. Produce a smaller baseline and expansion triggers.',
 'Start with a justified compute option, PostgreSQL, private object storage, necessary background work, and basic observability. Add tools for concrete replay, query, scale, or ownership needs. State what symptom/requirement would justify each expansion and what operations it adds.',
 'The DB is restored to yesterday but Kafka contains newer events. How do you reason about recovery?',
 'Identify authoritative facts, restored outbox/consumer inbox state, event retention, and projection rebuild policy. Reconcile duplicates and missing local state deliberately. Do not blindly replay every external side effect. Test a synthetic restore/replay timeline.',
 [q('Must every Rails app run both ECS and EKS?','Yes','No, they can be alternative operating models','Only with S3',1,'Select a justified compute/orchestration choice.'),q('What should each journey identify?','Its durable success boundary and recovery path','Only product logos','Only the happy-path HTTP status',0,'Completion meaning changes across boundaries.'),q('What should justify a new infrastructure tool?','A concrete requirement and operating capacity','Its popularity alone','A larger architecture diagram',0,'Every tool adds responsibility as well as capability.')],
 'Trace the journey, not the logos.', ['User identity and edge','Web and authoritative DB','Object/job/event boundary','Independent consumers','Observed recovery and cost'], [('AWS Well-Architected',AWS+'wellarchitected/latest/framework/welcome.html')],usecase='A holistic architecture explanation and cloud design interview/work review.',benefits='Connects services to user journeys and operating decisions.',drawbacks='The full design is a learning reference; a small product should select only justified parts.',tags=['aws','architecture','capstone'])
chapter('ops','docker-model','Docker: image, container, process, and volume','beginner',
 'Reconstruct what survives stop, restart, replacement, and image rebuild.',
 '''An image is a packaged filesystem/configuration template. A container is a running or stopped instance with its own writable layer. It runs processes using the host kernel’s container facilities; it is not automatically a whole independent virtual machine.

Stopping a container is different from replacing/removing it. Important state should live in a deliberately managed volume or external service, not accidentally in the writable layer. A bind mount connects a host path; a named volume has a separate lifecycle.

Use Docker to make runtime dependencies and process startup reproducible. It does not fix application permissions, data backups, or unsafe code. Learn the process, filesystem, network, and identity boundaries separately.''',
 '''```sh
# Local training containers only.
docker image inspect ruby:3.3-slim
docker ps --filter label=com.docker.compose.project=learning-event-lab
docker compose -p learning-event-lab ps
docker compose -p learning-event-lab logs --tail=50 web
```

Use the lab compose file from its directory. Do not run cleanup against all containers or volumes on your machine.''',
 '''Build image → create container → start main process → write to layer/volume → stop → restart or replace. Before each step, predict which bytes and process state remain.

Trace a Rails upload written locally. A replacement container starts from the image again; it does not inherit the old writable layer. External object storage solves a different boundary from packaging.''',
 'EXPOSE documents a container port; it does not publish it to the host. A running container can contain a failing app. A volume is not itself a tested backup.',
 'A report file disappears after redeploying the container. Explain the storage boundary and repair it.',
 'The file lived in the replaced writable layer. Store important artifacts in an explicit volume/object service with ownership and recovery policy. Keep only disposable temp files local. Test replacement rather than only restart.',
 'An image works on one machine but not another CPU architecture. What must be explicit?',
 'The image platform/architecture and native dependencies. Build/publish supported variants or choose the correct platform deliberately. Containers package userspace, not a universal hardware emulator.',
 [q('What is an image?','A template/artifact for container instances','A running process only','A database backup',0,'Image and instance have different lifecycles.'),q('Does EXPOSE publish a host port?','Yes','No','Only for Rails',1,'Host port mapping is a separate runtime setting.'),q('What should survive replacement deliberately?','Important state outside the disposable layer','Every process memory value','Only logs left inside the old container',0,'Persist/recover data explicitly.')],
 'Image is the recipe. Container is the instance. Volume is a data decision.', ['Image artifact','Container instance','Main process','Writable layer or volume','Restart versus replacement'], [('Docker containers','https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/')],usecase='Remembering Docker by lifecycle instead of command memorization.',benefits='Reproducible runtime packaging.',drawbacks='State, platform, access, and recovery still need explicit design.',tags=['docker','fundamentals'])

chapter('ops','docker-build','Docker builds: layers, identity, and a smaller runtime','intermediate',
 'Build a Rails artifact without embedding secrets or relying on mutable tags.',
 '''A Dockerfile records image construction. Layer caching can speed repeated builds when stable dependency steps occur before frequently changing app files. A .dockerignore keeps unnecessary/private content out of the build context.

Use a deliberately selected base and dependency lockfile. Multi-stage builds can keep compilers out of the runtime image. Run the app with a non-root user when its runtime needs permit. Pass secrets through supported build/runtime mechanisms rather than copying them into layers.

The main process needs signal handling and graceful shutdown. Shell wrappers can change how signals reach the app. Use an exec-style command or an entrypoint that execs the application. Image size matters, but a tiny unmaintainable image is not the goal.''',
 '''```dockerfile
FROM ruby:3.3-slim
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
```

This is a teaching shape, not the complete lab Dockerfile. Add required system libraries, user/permissions, .dockerignore, and a deliberate release image/digest policy. Never COPY the work project or its secrets into this lab.''',
 '''Build context → dependency layers → app layer → runtime command → registry digest. Change only a source file and inspect which layers rebuild. Then change a gem lock and predict the invalidation.

During stop, SIGTERM should reach the process so it can stop taking work and finish or abandon it safely within the orchestrator’s grace period.''',
 'Deleting a secret in a later layer does not erase it from earlier layers. A mutable base/tag can change rebuild output. A shell that does not exec can interfere with signal forwarding.',
 'A build copies .env, then removes it in the next RUN command. Why is that insufficient?',
 'The secret may remain in an earlier image layer/build context/cache. Exclude it from context and use supported secret delivery. Rotate any exposed secret through the appropriate human/operational process; deleting a file is not revocation.',
 'The app ignores graceful shutdown after container stop. What do you inspect?',
 'Inspect PID 1/entrypoint command, signal forwarding, app server shutdown configuration, and termination grace period. Test an in-flight request/job in the local lab. Do not rely on a forced kill as ordinary shutdown.',
 [q('Does later rm erase a copied secret from prior layers?','Yes','No','Only with slim images',1,'Layer history can retain it.'),q('What should enter the dependency layer before source?','Gemfile and lockfile when appropriate','Every temporary log','Production credentials',0,'Stable dependency inputs improve useful caching.'),q('Why prefer exec-style process startup?','Clear signal delivery to the app process','Automatic SQL transactions','Unlimited memory',0,'Lifecycle behavior depends on the main process.')],
 'Cache stable inputs. Keep secrets out. Let signals reach the app.', ['Build context','Dependency layers','App source','Runtime identity and command','Immutable image'], [('Docker build practices','https://docs.docker.com/build/building/best-practices/')],usecase='Rails image delivery and predictable rebuilds.',benefits='Faster repeat builds and clearer runtime boundaries.',drawbacks='Native dependencies, patching, and reproducibility need maintenance.',tags=['docker','delivery'])

chapter('ops','compose','Compose: connect web, database, broker, and workers','beginner',
 'Explain service DNS, ports, volumes, health, and startup versus readiness in a local application.',
 '''Compose describes a multi-container application. Services can reach one another by service name on their configured network. localhost inside a container refers to that container, not the database next door or your host browser.

Published host ports and container service ports are different. The browser may use localhost:3300 while the worker uses web:3000. Kafka also advertises broker addresses to clients, so correct bootstrap reachability alone is not enough.

depends_on ordering is not universal application readiness. Use health checks/conditions where supported and keep client startup/retry behavior deliberate. Name volumes and project scope so a lab does not collide with another application. Read the cleanup command before removing any volume.''',
 '''```yaml
services:
  web:
    build: .
    ports: ["127.0.0.1:3300:3000"]
    environment:
      DATABASE_URL: postgres://learning:learning-only@db:5432/tickets
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: learning
      POSTGRES_PASSWORD: learning-only
      POSTGRES_DB: tickets
```

This small fragment omits persistence/health to make those decisions visible. Use the complete event lab for the tested setup; credentials here are synthetic local training values.''',
 '''Compose creates network/services → database becomes healthy → schema setup completes → web/dispatch/consumer start → service DNS connects internal calls → published port serves the browser.

Inspect logs and exit status per service. Rebuilding an image does not necessarily replace every running service unless the chosen command does so. State what the command will change.''',
 'Using localhost for db from web points at the wrong container. Removing volumes erases local lab data. A started DB process may still be initializing or lack the schema.',
 'The worker cannot reach Kafka because it uses localhost:19092. Repair the internal/external address model.',
 'Use the broker’s internal service address from containers and the published external address from host clients, with advertised listeners matching each network. Verify metadata endpoints are reachable from the client’s location.',
 'A web container starts before migrations finish. What readiness/startup contract helps?',
 'Use a deliberate setup/migration step, suitable health/dependency conditions, and app startup behavior that reports failure clearly. Avoid running competing migrations in every replica. Test a clean first start and a restart with existing data.',
 [q('localhost inside a worker refers to what?','The worker container itself','Every service in Compose','Always the host',0,'Use service DNS for peer containers.'),q('Startup order proves readiness?','Always','No','Only with YAML',1,'The dependency may still be initializing or missing schema.'),q('What scopes the lab’s resources?','A deliberate Compose project name','The current browser title','The Rails model name',0,'Project scoping helps avoid collisions.')],
 'Know which network the client is standing in.', ['Compose project','Service DNS','Dependency readiness','Internal connection','Published browser port'], [('Compose application model','https://docs.docker.com/compose/intro/compose-application-model/')],usecase='A repeatable Rails/Postgres/Kafka development lab.',benefits='Connected local services in a reviewable file.',drawbacks='Networking and readiness still require understanding.',tags=['docker','compose'],lab='rails-kafka')

chapter('ops','kubernetes-model','Kubernetes: desired state, pods, and controllers','beginner',
 'Explain how a Deployment leads to running pods and what happens when one disappears.',
 '''Docker packages/runs containers. Kubernetes coordinates desired workloads through an API and controllers. It can use compatible container runtimes; Docker Engine is not a required node runtime for every cluster.

A Pod groups containers that share a lifecycle/network context. A Deployment manages a ReplicaSet and replaceable Pods for suitable workloads. You usually change the desired specification rather than manually repairing a particular pod.

Requests/limits, probes, identity, configuration, and storage affect whether a workload can run usefully. Kubernetes does not know your business transaction rule. A replacement pod can repeat work if the job/consumer boundary is not designed for it.''',
 '''```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: tickets-web}
spec:
  replicas: 2
  selector: {matchLabels: {app: tickets-web}}
  template:
    metadata: {labels: {app: tickets-web}}
    spec:
      containers:
        - name: web
          image: learning/tickets:chosen-version
          ports: [{containerPort: 3000}]
```

This manifest fragment needs a real image, configuration, resource policy, and probes. It is not automatically applied to any cluster.''',
 '''Submit desired state → controller creates/adjusts ReplicaSet → scheduler chooses capacity → kubelet/runtime starts containers → readiness decides traffic eligibility. Remove one lab pod and observe reconciliation, not manual resurrection of the same identity.

Inspect events when a pod is Pending or repeatedly restarting. Image pull, scheduling, process failure, and readiness failure are different states.''',
 'A pod is disposable identity, not your only copy of data. Increasing replicas does not make a database transaction safe or a queue effect unique.',
 'A developer edits a running container to fix a file, then the fix vanishes after rescheduling. Repair the delivery model.',
 'Change the source/configuration, build a new identified artifact or update the managed config, and roll out the desired specification. Treat manual pod edits as temporary diagnostics, not durable deployment state.',
 'A pod stays Pending with no app logs. What should you inspect before debugging Rails?',
 'Inspect scheduling events, resource requests/capacity, node constraints, volume attachment, and image/setup state. The process may never have started, so Rails logs cannot explain every pod state.',
 [q('What does a Deployment express?','Desired replaceable workload state','A universal data backup','Only a shell session',0,'Controllers reconcile the declared workload.'),q('Must Kubernetes use Docker Engine on every node?','Yes','No','Only for Ruby',1,'It uses compatible container runtime interfaces.'),q('Do replicas prevent duplicate business effects?','Yes','No','Only with two pods',1,'Application processing still needs its own correctness rules.')],
 'Declare the state. Observe reconciliation. Keep data responsibility explicit.', ['Deployment desired state','ReplicaSet','Scheduled Pod','Container process','Readiness and replacement'], [('Kubernetes overview','https://kubernetes.io/docs/concepts/overview/'),('Deployments','https://kubernetes.io/docs/concepts/workloads/controllers/deployment/')],usecase='Remembering Kubernetes from its control loop.',benefits='Declarative workload replacement and orchestration.',drawbacks='Workload correctness and platform operations remain.',tags=['kubernetes','fundamentals'])

chapter('ops','kubernetes-network','Kubernetes networking: Services, selectors, ingress, and names','intermediate',
 'Trace a request from edge to a ready pod and debug an empty Service endpoint set.',
 '''Pods can be replaced and their addresses can change. A Service gives a stable access abstraction for matching endpoints. Selectors connect the Service to labelled Pods; a spelling mismatch can leave no endpoints.

Ingress or Gateway-related resources describe external routing under a selected controller implementation. Defining an Ingress object does not install every required controller or cloud load balancer. The exact controller’s contract matters.

Map DNS, ports, targetPort, ready endpoints, network policy, and app listener separately. Inside a Pod, localhost refers to its network namespace. Reaching a peer service uses the service name, not the browser’s public URL by habit.''',
 '''```yaml
apiVersion: v1
kind: Service
metadata: {name: tickets-web}
spec:
  selector: {app: tickets-web}
  ports:
    - port: 80
      targetPort: 3000
```
```sh
kubectl get pods -l app=tickets-web
kubectl get service tickets-web
kubectl get endpointslices -l kubernetes.io/service-name=tickets-web
```

Run only against a deliberately selected training context/namespace.''',
 '''Client/edge → controller route → Service port → selected ready Pod endpoint → app target port. A 503 can come from no eligible endpoints even when a pod process exists.

Test a selector mismatch, wrong targetPort, and readiness failure separately. Observe how each changes events/endpoints/response. Keep the app’s allowed-host/proxy/TLS configuration in the path.''',
 'A container listening only on 127.0.0.1 may not accept the intended Pod-network traffic. An Ingress without its controller is only desired routing data.',
 'Pods run but the Service has no endpoints. What do you inspect?',
 'Compare selectors/labels, namespace, readiness conditions, and endpoint slices. Then inspect ports/listener/network policy. Do not immediately expose every port or bypass the Service permanently.',
 'The route works by port-forward but not through ingress. What boundary did the test bypass?',
 'Port-forward bypasses parts of edge/controller/Service routing and policy. Inspect controller installation/configuration, route match, TLS/host, endpoints, and target health. A debug shortcut is not an end-to-end test.',
 [q('What connects a Service to ordinary selected Pods?','Labels/selectors and endpoint readiness','The container image title','A database ID',0,'A mismatch can produce no endpoints.'),q('Does defining Ingress install its controller?','Automatically','No','Only on a laptop',1,'Implementation must exist and be configured.'),q('Does port-forward prove ingress works?','Yes','No','Only over HTTP',1,'It bypasses parts of the real traffic path.')],
 'Name → route → Service → ready endpoint → listener.', ['External route','Installed controller','Service selector','Ready endpoint','App listener'], [('Kubernetes Services','https://kubernetes.io/docs/concepts/services-networking/service/'),('Ingress','https://kubernetes.io/docs/concepts/services-networking/ingress/')],usecase='Debugging healthy-looking pods with broken traffic.',benefits='Stable service access across pod replacement.',drawbacks='Several routing layers can fail independently.',tags=['kubernetes','networking'])

chapter('ops','kubernetes-release','Kubernetes probes, resources, rollout, and graceful work','intermediate',
 'Choose startup/readiness/liveness signals and release web/worker code without confusing restart with recovery.',
 '''Startup, readiness, and liveness ask different questions. Startup protects a slow initialization phase. Readiness controls traffic eligibility. Liveness can trigger a restart when the process is stuck under the chosen health contract.

Do not make liveness depend on every remote service; an outage can cause a restart storm. A worker also needs a progress/processing health model, not necessarily the web app’s HTTP probe.

Resource requests affect scheduling; limits affect runtime behavior under the selected resource type. CPU throttling and memory termination can look like app bugs. A rollout needs compatible schema, ready new pods, graceful old-pod shutdown, and an explicit rollback/data plan.''',
 '''```yaml
startupProbe:
  httpGet: {path: /live, port: 3000}
  failureThreshold: 30
  periodSeconds: 2
readinessProbe:
  httpGet: {path: /ready, port: 3000}
livenessProbe:
  httpGet: {path: /live, port: 3000}
resources:
  requests: {cpu: "100m", memory: "256Mi"}
  limits: {memory: "512Mi"}
```

Illustrative values only: measure the actual Rails startup, memory, and traffic. Do not paste arbitrary limits into production.''',
 '''New specification → new pods start → startup check → readiness allows traffic → old pods drain → process receives termination signal → unfinished work completes or becomes safely retryable. Observe rollout and user-level error/latency.

If a worker is terminated after DB commit but before offset/queue acknowledgement, its replacement may repeat the item. Infrastructure shutdown and business idempotence must cooperate.''',
 'A probe that requires login can fail every pod. Tight memory limits can cause repeated OOM termination. A code rollback does not reverse a destructive migration.',
 'A provider outage makes liveness fail and every pod restarts repeatedly. Repair the health contract.',
 'Keep liveness focused on process recoverability. Model the dependency in readiness or asynchronous backlog according to the product contract, with bounded timeouts. Monitor the actual failure rather than using restarts as a universal repair.',
 'A rollout kills consumers mid-event. What must the consumer/shutdown design ensure?',
 'Stop taking new work, handle in-flight work within a bounded grace period, and commit acknowledgement only after the durable effect. Expect repetition after forced termination and make it safe. Test shutdown at the effect/ack gap.',
 [q('Which probe controls traffic eligibility?','Readiness','Only liveness','Only startup',0,'Readiness says whether the pod should receive traffic now.'),q('Should every provider failure force a restart?','Always','No','Only in Kubernetes',1,'Restarting can amplify an external outage.'),q('What can memory limit termination resemble?','An unexplained process crash','Automatic successful retry','A TLS error only',0,'Inspect termination reason and resource evidence.')],
 'Start safely. Route when ready. Restart only for a reason.', ['Measured resources','Startup contract','Readiness traffic','Graceful rollout','Repeat-safe recovery'], [('Kubernetes probes','https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/')],usecase='Rails web/worker deployment and incident diagnosis.',benefits='Controlled traffic and process lifecycle.',drawbacks='Poor probes/limits can create outages themselves.',tags=['kubernetes','delivery','reliability'])

chapter('ops','redis-types','Redis foundations: pick a data structure for the question','beginner',
 'Choose strings, hashes, sets, sorted sets, lists, and streams from access patterns.',
 '''Redis is a networked data-structure service, not just a faster hash in your Ruby process. Each operation has a data type, cost, key scope, and failure behavior. Keep network round trips and memory in mind.

Strings fit values/counters. Hashes fit fields under one key. Sets answer membership/uniqueness. Sorted sets rank members by score. Lists model ordered pushes/pops. Streams provide a retained entry structure with consumer-group features. Pub/Sub is a different live-delivery contract and should not be mistaken for a durable queue.

Name keys with scope and purpose. Decide expiry deliberately. Use SCAN-style iteration for operational browsing rather than blocking a large server with a casual KEYS *. An atomic command is not the same thing as an atomic multi-command business workflow.''',
 '''```text
SET learning:ticket:42:summary "open" EX 60
HSET learning:ticket:42 title "Export fails" status open
SADD learning:workspace:7:watchers user-1 user-2
ZADD learning:workspace:7:priority 8 ticket-42
INCR learning:metrics:completed
```

These are Redis command examples for an isolated lab. Observe TYPE, TTL, and expected result. A wrong-type error is useful feedback about your data model.''',
 '''Choose a question → choose a structure/key → execute a bounded operation → inspect result/TTL → define rebuild or persistence. Compare one command with read-modify-write in application code.

INCR is atomic as that command. GET followed by SET from two clients can lose an update. A string counter also needs a policy for expiry and retry.''',
 'A set’s uniqueness does not coordinate a PostgreSQL write automatically. A key with no expiry can grow forever. Pub/Sub messages can be missed by disconnected subscribers under its contract.',
 'A team uses GET, adds one in Ruby, then SET for a shared counter and loses increments. Repair it.',
 'Use an atomic counter operation or an explicit atomic script/transaction design for the full rule. Test two clients. Also define duplicate command handling if the same logical increment can be retried after a timeout.',
 'A leaderboard needs top scores and tie behavior. What should be defined beyond choosing a sorted set?',
 'Define score updates, tie ordering, identity scope, expiry/rebuild, and whether Redis is authoritative or a projection. Test equal scores and repeated events. A sorted set chooses an access structure, not the business semantics.',
 [q('Which structure naturally supports ranked scores?','Sorted set','Only a plain string','A CSS grid',0,'Sorted sets associate members with scores.'),q('GET then SET is one atomic business operation?','Yes','No','Only for integers',1,'Other clients can interleave between commands.'),q('Pub/Sub automatically stores missed messages for offline clients?','Yes','No','Only with JSON',1,'Live Pub/Sub and retained streams/queues have different contracts.')],
 'Ask the query, then choose the structure.', ['Access question','Scoped key','Data structure','Atomic command','TTL and recovery'], [('Redis data types','https://redis.io/docs/latest/develop/data-types/'),('Redis Pub/Sub','https://redis.io/docs/latest/develop/pubsub/')],usecase='Counters, memberships, ranked projections, and caches.',benefits='Useful atomic data operations and low-latency access.',drawbacks='Memory, round trips, key lifecycle, and cross-store consistency remain.',tags=['redis','fundamentals'],lab='redis')

chapter('ops','redis-cache','Redis caching: freshness, invalidation, and stampedes','intermediate',
 'Design cache-aside with scoped keys and bounded rebuild behavior.',
 '''Cache-aside reads a copy if present, otherwise loads from the authority and stores a copy. The hard questions are which values may be stale, for how long, and how a write changes the cached answer.

Include tenant, query, and relevant version dimensions in keys. A TTL limits some stale lifetimes but does not prove immediate revocation or prevent old data being refilled after a race. Permission-sensitive checks may need a fresh authority boundary separate from cached content.

When many keys expire together, requests can stampede the database. Use bounded rebuilds, jittered expiries, request coalescing, and stale-serving policies only where the product allows them. A cache outage should not create unlimited fallback work.''',
 '''```ruby
key = "workspace:#{workspace_id}:ticket:#{ticket_id}:v#{version}"
# Rails.cache.fetch(key, expires_in: 60) { load_allowed_summary }
```

The loader and key must use trusted scope. A versioned key helps only if the reader knows the current version through a reliable path. Do not make version lookup cost or authorization disappear from the diagram.''',
 '''Read miss → DB load → cache fill. Now interleave a write: A reads old DB, B commits new DB and deletes cache, A fills old value. A simple “delete after write” rule can still have a stale-fill race.

Choose a consistency policy that matches the requirement: tolerate bounded staleness, version entries, use guarded refresh, or read the authority for strict decisions. Test the chosen timeline.''',
 'TTL is not a universal correctness proof. Caching a denied/allowed result without proper context can leak access. Cold-cache fallback can collapse the authority.',
 'Private-ticket access is revoked but a cached permission stays valid for an hour. Repair according to a two-second revocation requirement.',
 'Use a permission path/version/invalidation design that actually meets the two-second requirement, with current authorization checked separately if necessary. Test cached reads immediately after revocation across users/workspaces. A one-hour TTL is incompatible with the stated rule.',
 'The cache is flushed and PostgreSQL is overloaded. How should rebuilding be bounded?',
 'Limit concurrent rebuilds, stagger expiry, coalesce duplicate loads, and serve a permitted stale value only under an explicit policy. Monitor fallback pressure and prioritize critical paths. Do not let every request independently rebuild the same expensive query.',
 [q('What is the source of truth in ordinary cache-aside?','The authoritative store','Always Redis','The browser cache',0,'The cache is a copy under a freshness policy.'),q('Does delete-after-write remove every stale-fill race?','Yes','No','Only with a long TTL',1,'An earlier reader can refill old data after deletion.'),q('What can synchronized expiry cause?','A stampede at the authority','Guaranteed balanced load','Automatic access revocation',0,'Many misses can synchronize expensive rebuilds.')],
 'Cache content. State freshness. Keep permission honest.', ['Scoped key','Hit or miss','Authoritative load','Bounded fill/invalidation','Freshness and recovery'], [('Redis eviction','https://redis.io/docs/latest/develop/reference/eviction/'),('Rails caching','https://guides.rubyonrails.org/v4.2/caching_with_rails.html')],usecase='Ticket summaries and expensive dashboard reads.',benefits='Reduces repeated authority work.',drawbacks='Freshness races and fallback pressure can be harder than the lookup itself.',tags=['redis','cache','correctness'],lab='redis')

chapter('ops','redis-correctness','Redis correctness: persistence, atomic work, and lock expiry','intermediate',
 'Explain pipeline versus transaction/script, persistence loss windows, and why a lease needs stale-writer protection.',
 '''A pipeline batches network operations for efficiency; it does not by itself make them one indivisible business operation. MULTI/EXEC and scripts provide different atomic-execution tools, but Redis transactions do not behave like a relational transaction with automatic rollback of every runtime error.

Persistence and replication are separate from command atomicity. RDB snapshots and AOF policies have different recovery/loss/performance tradeoffs. A replica/failover configuration can still have a data-loss window under its contract. Select it from the role of the data, not the word persistent alone.

A lock with an expiry is a lease. Worker A can pause, its lease expire, and worker B acquire it. A can resume as a stale owner. Use the authority’s conditional write/version or fencing design where correctness requires excluding stale writers. A random token and compare-delete protect release ownership, not every business write.''',
 '''```text
Bad release: DEL lock:key, regardless of owner
Better ownership release: compare stored token, then delete atomically

Still possible:
A lease expires → B owns lease → A resumes → stale A writes elsewhere
```

For inventory or money, prefer a rule enforced at the authoritative database boundary where feasible. Do not use a short Redis TTL as proof of global mutual exclusion.''',
 '''Trace acquire → pause → expiry → new owner → old owner resumes. Identify which downstream store can reject the old write. Then trace a Redis crash and ask what persisted/replicated data is actually recoverable.

Test the failure model in the isolated lab. Measure the selected durability policy’s behavior, and document what data can be rebuilt versus what needs reconciliation.''',
 'Atomic commands do not make external effects atomic. Pipeline success is not a database commit. A lock release can delete another owner’s lock if token ownership is not checked.',
 'A report worker pauses longer than the lock TTL and two workers publish the same report. Repair the business rule.',
 'Use a unique report-run identity/constraint and idempotent publication or an authority-side version/fencing mechanism. Release leases only when the token matches. Test the expired-owner timeline, not just two fast lock acquisitions.',
 'You enable AOF and call queued jobs perfectly durable. What else must be specified?',
 'The fsync policy, replication/failover behavior, acknowledged-write loss window, backups/restore, memory/eviction policy, and job reconciliation source. Persistence is a configuration contract, not an absolute word.',
 [q('A pipeline guarantees a multi-command atomic business operation?','Yes','No','Only with many commands',1,'It primarily reduces round trips.'),q('Can an expired lock owner resume later?','Yes','No','Only in Java',0,'Pauses can outlast a lease.'),q('Does compare-delete alone fence writes to PostgreSQL?','Yes','No','Only with UUID tokens',1,'Release ownership and downstream stale-write rejection are separate.')],
 'Atomic here is not atomic everywhere. A lease can expire.', ['Command boundary','Persistence policy','Lease ownership','Stale-owner timeline','Authority-side rule'], [('Redis transactions','https://redis.io/docs/latest/develop/interact/transactions/'),('Redis persistence','https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/'),('Redis locks','https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/')],usecase='Distributed workers, counters, and critical lock-based coordination.',benefits='Prevents overclaiming what a fast coordination tool guarantees.',drawbacks='Strong correctness can require authority-side mechanisms beyond Redis.',tags=['redis','reliability','correctness'],lab='redis')

chapter('ops','datadog','Datadog: turn traces and monitors into an investigation','beginner',
 'Connect Rails requests, jobs, SQL, and provider calls with useful service identity and bounded telemetry.',
 '''Datadog combines observability capabilities such as infrastructure monitoring, APM, logs, and monitors. Choose the signals needed for a concrete investigation. Installing an agent alone does not make every request/job trace connected.

Use stable service, environment, and version tags. Instrument the relevant Rails/client/job libraries with versions supported by your runtime. Current datadog gem setup differs from legacy ddtrace setups; a Rails 4.2/Ruby 2.7 application needs a verified compatibility choice.

Setup path: choose supported tracer/agent versions, configure a training service identity and agent path, instrument a request and worker, correlate logs safely, define a useful monitor/runbook, and verify with a synthetic slow dependency. Review sampling, sensitive fields, ingestion, retention, and billing dimensions.''',
 '''```text
service=tickets-web, env=learning, version=<source revision>
trace: HTTP request → Rails use case → SQL → receipt provider
worker trace: saved event ID links asynchronous work deliberately
```

In a modern supported setup, configure instrumentation from the provider’s Ruby guide. Do not paste a current gem into the legacy work Gemfile. No telemetry is sent to an account by this course.''',
 '''User-visible latency spike → service latency/error metrics → slow trace → SQL or provider span → correlated safe logs → hypothesis → controlled repair → monitor recovery. Async boundaries need explicit context propagation/linking rather than assuming one synchronous stack.

An absent trace can mean sampling or missing instrumentation, not proof the request never ran.''',
 'Unbounded tags and full payload capture can create cost/privacy problems. A monitor without a clear action becomes noise. Trace instrumentation can be misconfigured even when infrastructure metrics arrive.',
 'You see host CPU but no Rails spans. What boundaries do you check?',
 'Check supported tracer version, app instrumentation load/configuration, service/env/version, agent endpoint/reachability, sampling, and the specific library integration. Verify a synthetic request. Host metrics and app traces are different collection paths.',
 'An event consumer is slow but the originating request looks fast. What should the investigation include?',
 'Queue/log lag and oldest event age, consumer processing traces, retry/error rate, and correlation via event ID/trace context. The request can finish before asynchronous work starts, so synchronous request latency alone misses the problem.',
 [q('Agent installed means every app span is present?','Always','No','Only on EC2',1,'Application instrumentation and transport must work too.'),q('What tags make release comparison useful?','Stable service, environment, and version','Every raw email address','Only host color',0,'Bounded identity connects signals to the deployed release.'),q('No trace proves no request ran?','Yes','No','Only when sampled',1,'Sampling and missing instrumentation can hide traces.')],
 'Start from the symptom, then follow a traceable boundary.', ['Service identity','Instrumentation and agent','Metrics and traces','Correlated diagnosis','Actionable monitor'], [('Datadog Ruby tracing','https://docs.datadoghq.com/tracing/trace_collection/dd_libraries/ruby/')],usecase='Investigating Rails/worker latency and release regressions.',benefits='Integrated signals and investigation workflows.',drawbacks='Compatibility, sampling, volume, cost, and sensitive-data policy need ownership.',tags=['observability','datadog'])

chapter('ops','opentelemetry','OpenTelemetry: instrumentation is not the storage backend','beginner',
 'Explain traces, metrics, logs, context propagation, and collector/exporter roles.',
 '''OpenTelemetry supplies standards, APIs/SDKs, instrumentation, and collection/export tools. It is not by itself the long-term observability database or dashboard. You still choose where telemetry is stored and how it is queried/retained.

A trace has spans describing work and relationships. Propagated context connects work across HTTP boundaries. An asynchronous event may carry context or link separate work under an explicit policy. Avoid putting sensitive business data into baggage that travels broadly.

Setup: select compatible instrumentation, stable resource attributes, a collector/exporter path, sampling/retention policy, and a test trace. Verify every hop and failure behavior. Telemetry failure should not accidentally block the main business operation without a deliberate reason.''',
 '''```text
Rails instrumentation → OTLP exporter → Collector
Collector: receive → process/redact/batch → export
Backend: storage, queries, dashboards, alerts
```

Record service.name, deployment environment, and version deliberately. Keep event IDs in suitable spans/logs; do not make every event a metric label.''',
 '''Request span begins → child SQL/client spans → context crosses a supported boundary → collector processes → backend receives → investigator queries. Inspect dropped/export-failed telemetry separately from application failures.

For a Kafka event, choose whether to propagate a trace context or use a span link, and keep event identity for business replay. Trace identity is not an idempotency key.''',
 'Choosing OTel does not eliminate backend cost. Baggage can spread sensitive values. A trace ID does not enforce exactly-once processing.',
 'The team installs OTel and expects dashboards without configuring an exporter/backend. Explain the missing path.',
 'Connect SDK/instrumentation to a configured exporter/collector and a storage/query backend. Verify a synthetic span end to end, then add dashboards/alerts for the task. Instrumentation is one part of the system.',
 'A consumer replays an old business event. Should its original trace ID be the deduplication key?',
 'No. Use a stable business event ID under a consumer-specific uniqueness rule. Trace context describes observation relationships and may be sampled or changed. Keep business correctness independent of telemetry.',
 [q('Is OTel alone a long-term query backend?','Yes','No','Only with Ruby',1,'You still choose storage/query/alerting.'),q('What connects distributed observation?','Context propagation/linking','A CSS ID','Only a DB index',0,'Spans need deliberate relationships across boundaries.'),q('Trace ID is the business event deduplication key?','Always','No','Only on replay',1,'Telemetry identity and business identity have different contracts.')],
 'Instrument → collect → export → store → investigate.', ['Application signal','Context','Collector processing','Chosen backend','Query and alert'], [('OpenTelemetry signals','https://opentelemetry.io/docs/concepts/signals/')],usecase='Portable instrumentation across services and observability vendors.',benefits='Common telemetry concepts and integration options.',drawbacks='Backend, volume, sampling, and privacy still need decisions.',tags=['observability','opentelemetry'])

chapter('ops','debezium','Debezium: capture committed changes without inventing business meaning','intermediate',
 'Explain CDC, snapshots, log positions, outbox routing, and duplicate-safe downstream processing.',
 '''Change data capture reads database changes through a supported source mechanism. Debezium connectors can take an initial snapshot and continue from a log position. This is useful for integration/projections, but a row change is not automatically a well-designed business event.

An outbox table stores a deliberate event with the business transaction. A connector/outbox router can publish that committed intent instead of relying on an application polling dispatcher. This changes the delivery machinery, not the need for schema, keys, deduplication, and recovery.

Setup concept: verify database/connector versions, required replication/log settings and privileges, snapshot/log retention, connector offsets/state, outbox schema/routing, and monitoring. CDC can retain database logs when it stops; monitor the source as well as Kafka.''',
 '''```text
Rails transaction: ticket update + outbox row
PostgreSQL committed log → Debezium connector
Outbox routing → ticket-events keyed by aggregate identity
Reporting consumer → inbox + projection transaction
```

The course’s runnable lab uses a polling outbox dispatcher first so you can see the dual-write boundary. Debezium is an alternative publisher path, not an extra publisher that should also emit the same rows.''',
 '''Initial snapshot → catch-up log position → committed changes → routed records → consumer effects. Restart at the connector’s saved position and expect the selected delivery/recovery contract, including possible repeats.

Trace event_id from outbox row through connector/topic to the consumer inbox. Raw CDC delete/tombstone behavior and business cancellation semantics are different questions.''',
 'CDC may expose columns not intended for downstream systems if schema/filtering is careless. A stopped replication slot/log reader can grow retained WAL. Running both polling and CDC publishers without coordination can duplicate events.',
 'After adding Debezium, the old dispatcher still publishes every outbox row too. Repair the ownership.',
 'Choose one deliberate publishing path or a coordinated migration/cutover strategy. Preserve stable event IDs and duplicate-safe consumers. Test the cutover window and monitor source log retention plus downstream lag.',
 'The connector is down for hours and PostgreSQL disk usage grows. What path explains it?',
 'Inspect the configured replication/log retention mechanism and connector progress. A stalled reader can retain logs required for catch-up. Follow the database-specific recovery procedure and backfill implications rather than deleting state blindly.',
 [q('Does a raw row change automatically express a business event?','Yes','No','Only after JSON encoding',1,'Business meaning needs a deliberate schema/contract.'),q('What should a transactional outbox share with the business write?','The same DB transaction','Only a timestamp','Only the same log message',0,'The commit saves intent atomically with the change.'),q('Which source-side signal matters for a stopped connector?','Retained database log/WAL growth','Only frontend clicks','Only image size',0,'CDC can affect source storage and recovery.')],
 'Committed change is the source. Business meaning is your contract.', ['Business transaction','Outbox or selected rows','CDC position','Routed Kafka record','Repeat-safe projection'], [('Debezium outbox router','https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html'),('PostgreSQL connector','https://debezium.io/documentation/reference/stable/connectors/postgresql.html')],usecase='Search/reporting projections and deliberate event publication.',benefits='Captures committed changes without app-level network dual writes.',drawbacks='Connector state, source logs, schema exposure, and cutover require operations.',tags=['debezium','cdc','events'])

chapter('ops','cassandra','Cassandra: design the query before the table','intermediate',
 'Explain partition/clustering keys, bounded partitions, denormalization, and the tradeoff versus PostgreSQL.',
 '''Cassandra is a distributed wide-column database with a query-oriented data model. Start from the reads you need. Partition keys distribute/group data; clustering columns order rows within a partition under the table definition.

Do not port a normalized relational schema and expect arbitrary joins. You may store multiple tables/projections for different reads. That makes write/update coordination and repair part of the application design.

Keep partitions bounded. A workspace with years of events under one partition can become a hotspot or grow too large. Time bucketing is one possible strategy, with its own query cost. Consistency levels and replication settings affect the read/write/failure contract; they do not make every cross-row invariant transactional.''',
 '''```sql
CREATE TABLE ticket_events_by_day (
  workspace_id text, event_day date, occurred_at timestamp,
  event_id uuid, ticket_id text, kind text,
  PRIMARY KEY ((workspace_id, event_day), occurred_at, event_id)
) WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC);
```

This example serves one day-scoped event query. It is not a universal ticket schema or a replacement for relational ownership/transaction rules.''',
 '''Query need → partition key scope → bounded partition → within-partition order → replicas/consistency → result. Then trace the writes needed for a second access pattern and how projections are repaired.

Measure partition size/skew and the cost of fetching a range across buckets. A query that requires broad filtering may signal a mismatched model.''',
 'A very large/hot partition can dominate one path despite many nodes. ALLOW FILTERING is not a universal performance solution. Cross-table denormalization can leave inconsistent projections after failure.',
 'All events for the busiest workspace use one forever-growing partition. Propose a bounded model and its query tradeoff.',
 'Choose a bucket such as day plus workspace if it fits the read/volume, retain a deterministic clustering key, and define range-query fan-out/merge. Measure skew and partition sizes. Do not choose a bucket without the query and volume.',
 'The app mainly needs relational joins and multi-row business transactions at modest scale. Is Cassandra the default upgrade?',
 'No. PostgreSQL may fit better. Choose Cassandra for a justified distributed access/availability/scale pattern and an operating team able to manage its data model/repair. Popularity alone is not a requirement.',
 [q('What should drive Cassandra table design?','Specific access queries','An arbitrary normalized ER diagram alone','The UI color scheme',0,'Its model is query-oriented.'),q('What can an unbounded hot partition cause?','Skew and a bottleneck','Automatic even scaling','Universal ACID joins',0,'Distribution does not remove a hot key.'),q('Is Cassandra a default replacement for every relational app?','Yes','No','Only in cloud',1,'Choose from actual access/correctness needs.')],
 'Query first. Bound the partition. Plan the extra copies.', ['Read pattern','Partition key','Clustering order','Replica/consistency choice','Projection repair'], [('Cassandra data modeling','https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html')],usecase='High-volume query-specific event projections.',benefits='Distributed storage designed around known access patterns.',drawbacks='Denormalization, skew, consistency choices, and operations add responsibility.',tags=['cassandra','data-modeling'])

chapter('ops','sendgrid','SendGrid: accepted email is not delivered email','beginner',
 'Trace message intent, provider acceptance, delivery events, suppression, and retry uncertainty.',
 '''An email integration has several states: saved intent, attempted request, provider acceptance, recipient-server delivery, bounce, suppression, and user interaction. The API accepting a request does not prove the person received or read it.

Use a narrow adapter and store a logical notification identity. Authenticate the sending domain and configure the selected provider’s required settings. Keep secrets out of code and validate webhook signatures/replay policy using the provider’s supported mechanism.

Setup: choose a training/sandbox mode, verify sender/domain configuration, scope the API credential, define templates and minimal data, add signed event-webhook handling, and test accepted, rejected, bounced, duplicate-event, and timeout cases. This course sends no real email.''',
 '''```text
Ticket completed → notification intent in DB
Worker → provider request → accepted/provider message identity
Signed webhook → delivery/bounce/suppression event
DB status update keyed by provider event identity
```

Do not put free-text private ticket content into a demo template or telemetry. A fake adapter should simulate acceptance followed by timeout.''',
 '''Follow one notification ID through retries and provider events. A webhook can be repeated or arrive after another event. Define allowed state transitions from observed facts rather than assuming arrival order is perfect.

For a timeout, check provider-supported status/idempotency behavior before resending. If acceptance is unknown, record uncertainty and reconcile rather than asserting success or failure without evidence.''',
 'A delivered event does not prove the human read the message. Tracking opens can have privacy/client artifacts. Webhook bodies alone are not proof of sender authenticity.',
 'The worker marks delivered immediately after API acceptance, then bounces are ignored. Repair the state model.',
 'Use accepted and delivered as separate states, process authenticated provider events idempotently, and expose bounce/suppression outcomes. Preserve logical notification identity and retry uncertainty. Test duplicate and out-of-order events.',
 'The provider accepted the send but the client timed out. What should a retry policy consider?',
 'The remote effect may already exist. Use any supported provider identity/reconciliation mechanism, deduplicate local intent, and tolerate or escalate ambiguity. Do not assume every email API offers a universal idempotency key.',
 [q('API acceptance proves human receipt?','Yes','No','Only with HTML mail',1,'Transport states and human behavior differ.'),q('How should repeated webhooks be handled?','Idempotently by event identity','Always applied as new business actions','Deleted before validation',0,'Delivery notifications can repeat.'),q('What must authenticate a webhook?','The provider-supported verification mechanism','Only a familiar JSON field','Only its event name',0,'Outside data is not inherently trusted.')],
 'Saved → accepted → delivered are different promises.', ['Durable notification intent','Provider attempt','Acceptance or unknown','Verified webhook','Idempotent status update'], [('SendGrid event webhook','https://www.twilio.com/docs/sendgrid/for-developers/tracking-events/event'),('SendGrid sandbox','https://www.twilio.com/docs/sendgrid/for-developers/sending-email/sandbox-mode')],usecase='Operational notifications and receipt-status tracking.',benefits='Managed delivery integration and delivery feedback.',drawbacks='Remote uncertainty, reputation/suppression, and webhook correctness remain.',tags=['sendgrid','email','integration'])

chapter('ops','cron','cron and scheduled work: a trigger is not a transaction','beginner',
 'Read a schedule and design missed-run, overlap, timezone, and deduplication behavior.',
 '''cron evaluates calendar schedules and starts commands in its environment. It does not ensure the previous run finished, that the command succeeded, or that a missed business period is repaired. Environment variables, working directory, shell, and timezone can differ from your interactive terminal.

Make the logical run explicit: daily-report(workspace, business_date). A unique database key and retry-safe use case protect duplicate triggers. Decide catch-up behavior after downtime and how DST/local-time rules apply.

For distributed deployments, choose one scheduler ownership strategy or an orchestrator schedule with a documented concurrency/missed-run policy. Still keep business deduplication. Logs/exit status and oldest expected-run age should reveal silent failures.''',
 '''```cron
# Example: 02:15 in the scheduler's configured timezone.
15 2 * * * /app/bin/run-daily-report
```

The wrapper should set its expected environment, call the application use case, and return an honest exit status. It should not rely on a developer’s current directory or shell profile.''',
 '''Calendar tick → process environment → command → unique business run → durable work → completion/failure. On restart after a day of downtime, decide whether the app enumerates missing periods or intentionally skips them.

Test overlap, duplicate scheduler instances, failed exit, and late starts. A log saying command started is not proof a report completed.''',
 'Two replicas can run the same schedule. A local file lock does not necessarily coordinate separate hosts. DST can make a local scheduled time absent or repeated.',
 'A daily report silently stops after deployment because cron has no Bundler environment. Repair observability and execution context.',
 'Use an explicit wrapper/runtime path and environment, capture failure exit/logs, and monitor expected-run completion age. Add a synthetic invocation check after deployment. Keep run deduplication and catch-up rules in the application.',
 'The business asks for every missed day to be regenerated after downtime. What belongs in code?',
 'Enumerate expected periods under the intended timezone, claim each unique run, and process idempotently with bounded catch-up. The scheduler trigger alone does not know which business periods are missing.',
 [q('cron ensures the previous run is done?','Always','No','Only for daily jobs',1,'Overlap policy must be implemented/selected.'),q('What identifies one logical daily report?','Scope plus intended business date','The process PID','The current log line',0,'Duplicate triggers should map to the same run.'),q('A started log proves completion?','Yes','No','Only with cron',1,'Observe the final business outcome.')],
 'Schedule the trigger. Persist the run. Observe completion.', ['Calendar and timezone','Known process environment','Unique run claim','Bounded work','Missed-run recovery'], [('POSIX crontab','https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html'),('Kubernetes CronJobs','https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/')],usecase='Reports, reminders, and periodic repair/reconciliation.',benefits='Simple calendar triggering.',drawbacks='Overlap, downtime, environment, and business success remain separate.',tags=['cron','scheduling'])

chapter('ops','pendo','Pendo: measure meaningful product behavior','beginner',
 'Define a product event and separate analytics identity, consent/data policy, and business success.',
 '''Pendo supports product analytics/guidance capabilities, including configured Track Events. Define what an event means before instrumenting it. A clicked button, an accepted request, and a completed business action are different events.

Choose stable names and a minimal property schema. A support app might record TicketAssignmentCompleted with method and outcome category, rather than every typed title or description. Visitor/account association and data collection settings must match the product’s privacy/access policy.

Setup: choose a training application/configuration, establish identity and collection policy, instrument one deliberate event after the relevant boundary, verify it arrives, and compare it with the actual business outcome. Keep server-side secrets out of the browser and source. This course sends no analytics to Pendo.''',
 '''```js
// Only after the relevant confirmed outcome and SDK readiness.
pendo.track('TicketAssignmentCompleted', {
  method: 'bulk', outcome: 'partial_success', schemaVersion: 1
})
```

Do not include private ticket text. Handle SDK loading/failure so analytics does not break the main task. A frontend event can be missed and is not the authoritative assignment record.''',
 '''Task action → confirmed application state → minimal event → SDK/server transport → associated analytics record → defined funnel/metric. Inspect missing events for SDK readiness, network/collection settings, naming, and selected analytics scope.

Compare analytics completion with a safe aggregate of the authoritative business outcome. Ad blockers, failures, or instrumentation gaps can change the measured population.''',
 'Client telemetry can be absent or repeated. A click funnel can reward confusion. Copying entire form data into event properties creates unnecessary exposure.',
 'The team records AssignClicked as task completion and sees a high success rate despite failed requests. Repair the event/metric.',
 'Separate attempted interaction from confirmed/partial/failed outcome, define denominator/time window, and reconcile with the business source where appropriate. Preserve a minimal event schema and verify collection gaps.',
 'A third-party SDK is unavailable. Should ticket saving fail?',
 'Usually no: isolate nonessential telemetry failure from the core action, record a safe local diagnostic if needed, and accept that analytics has a gap. Decide any required audit trail separately in the application authority.',
 [q('A button click proves business completion?','Yes','No','Only with a Track Event',1,'The action may still fail later.'),q('What belongs in event properties?','Minimal intentional non-sensitive fields','Every free-text form value','API secrets',0,'Collect only data needed for the question.'),q('Is client analytics the authoritative business ledger?','Yes','No','Only with a dashboard',1,'Collection can be missing, duplicated, or manipulated.')],
 'Define the outcome before tracking the click.', ['Task boundary','Minimal event schema','Identity and collection policy','Verified transport','Meaningful metric'], [('Pendo Track Events','https://support.pendo.io/hc/en-us/articles/360032294151-Track-Events'),('Configure Track Events','https://support.pendo.io/hc/en-us/articles/360032294291-Configure-Track-Events')],usecase='Understanding feature adoption and operational task funnels.',benefits='Product behavior visibility and guidance workflows.',drawbacks='Instrumentation meaning, missing data, identity, and privacy need ownership.',tags=['pendo','analytics','ux'])

chapter('ops','terraform','Terraform: desired infrastructure with state and review','intermediate',
 'Explain configuration, plan, state, drift, and the effect of apply without treating a plan as a harmless toy.',
 '''Terraform describes resources through providers and tracks managed identity in state. Configuration is desired structure; state maps that structure to actual remote objects. A plan compares the chosen inputs/state/provider view with reality and proposes changes.

State can contain sensitive values. Use a deliberate backend/access/locking/recovery strategy. Two uncoordinated applies can race. Manual console changes create drift that must be understood before the next plan.

Learning setup: use a dedicated training configuration, pin provider/tool versions, review variables and account/region, run formatting/validation, inspect a saved plan, and apply only when you deliberately choose the real resource/cost changes. The course does not run apply or create AWS infrastructure.''',
 '''```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = var.region }
# Resource examples belong in the selected training account,
# with a reviewed backend, variables, tags, and cleanup plan.
```

This fragment is a configuration shape, not a complete production template.''',
 '''Configuration + variables + state + provider context → plan → human/team review → apply → refreshed state → observed service. A successful apply proves resources changed, not that Rails works end to end.

Before a replacement/destruction, inspect why the provider proposes it and which data/lifecycles are affected. Keep backups and recovery separate from state-file backups.''',
 'State is not an application database backup. Removing a resource block can propose deletion. A plan from the wrong account/variables is the wrong plan even if syntactically valid.',
 'A plan proposes replacing the database after a small refactor. What should happen before apply?',
 'Stop at the review boundary, inspect resource address/identity/provider changes, state mapping, lifecycle implications, and data recovery. Use supported moved/import procedures where appropriate. Do not apply merely because the command produced a plan.',
 'Someone changes a security group in the console. How should the next infrastructure change handle it?',
 'Detect and understand drift, decide intended state, update/reconcile through the team’s process, and review the resulting plan. Do not blindly overwrite a possibly important incident change or leave undocumented drift forever.',
 [q('What does Terraform state map?','Configuration resources to managed remote identity','All application data backups','Every browser event',0,'State tracks resource management identity and attributes.'),q('Does apply success prove Rails works?','Yes','No','Only with AWS provider',1,'Application validation is a separate layer.'),q('Can state contain sensitive values?','Yes','No','Only comments',0,'Backend/access/recovery need deliberate policy.')],
 'Plan the change. Protect state. Verify the service.', ['Configuration and variables','Managed state','Reviewed plan','Deliberate apply','Service validation and drift'], [('Terraform introduction','https://developer.hashicorp.com/terraform/intro')],usecase='Repeatable cloud infrastructure changes.',benefits='Reviewable configuration and resource change plans.',drawbacks='State, drift, provider behavior, and destructive changes require care.',tags=['terraform','infrastructure'])

chapter('ops','github-actions','GitHub Actions: test, build once, and promote an artifact','intermediate',
 'Design a CI/CD path with explicit permissions, artifact identity, and release gates.',
 '''A workflow is triggered by an event and runs jobs/steps on runners. CI should produce relevant evidence for a change: type checks, tests, build, and selected integration checks. CD promotes a known artifact into an environment under deliberate permissions.

Build once from a known revision and record the image digest. Do not rebuild independently for staging and production and call them the same tested artifact. Cache dependencies for speed, but do not let a cache replace a lockfile or validation.

Choose narrow workflow permissions and supported temporary cloud identity where appropriate. Untrusted PR code must not receive powerful deployment secrets. Pin third-party actions according to the team’s supply-chain policy and review their access.''',
 '''```yaml
name: learning-checks
on: [pull_request]
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # training illustration; pin per policy
      - run: echo "Install pinned runtime, then run targeted checks"
```

The example explains structure only. The lab's local checks are not automatically published as a repository workflow or granted cloud access.''',
 '''PR event → least-privilege test job → passing evidence → identified artifact → deliberate environment gate → deployment → smoke/monitor → rollback decision. Keep credentials scoped to jobs/environments that need them.

Treat migration compatibility and external effects as release concerns. A green CI job cannot make a destructive data rollback reversible.''',
 'A build from a dirty local tree is not the CI-tested revision. Broad write permissions on untrusted workflows widen access. A deployment without a smoke check can be green while users fail.',
 'Production rebuilds the same tag after staging passed and gets different dependencies. Repair the artifact flow.',
 'Use locked dependencies and a controlled build from the known revision, record the immutable digest, and promote that artifact. Keep provenance and environment-specific config separate. Validate the deployed digest and smoke behavior.',
 'A PR from an untrusted fork needs tests. How should deployment access be handled?',
 'Run appropriate checks without privileged deployment secrets. Keep privileged promotion in a trusted, reviewed context with narrow permissions and environment gates. Do not execute untrusted code with broad cloud access.',
 [q('What should be promoted after testing?','The identified immutable artifact','A fresh unrelated rebuild','Only a branch nickname',0,'Testing evidence must connect to deployed bytes.'),q('Should every PR job have deployment secrets?','Yes','No','Only when tests are slow',1,'Untrusted code and privileged credentials must be separated.'),q('CI success alone proves deployment health?','Yes','No','Only for containers',1,'Environment wiring and runtime behavior need checks.')],
 'Test the revision. Build once. Promote known bytes.', ['Workflow trigger','Bounded permissions','Relevant checks','Immutable artifact','Gated deployment and smoke'], [('GitHub workflows','https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows'),('Actions security','https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions')],usecase='Rails/Vue delivery with reproducible artifacts.',benefits='Repeatable checks and reviewable promotion.',drawbacks='Runner trust, secrets, caches, and release compatibility need design.',tags=['ci','github-actions','delivery'])

chapter('ops','proxy-pools','Nginx and PgBouncer: two different kinds of front door','intermediate',
 'Distinguish HTTP reverse proxying from database connection pooling and test their compatibility limits.',
 '''Nginx can accept HTTP traffic and proxy it to application servers, serve suitable static content, and enforce selected request/timeout rules. It is not a database pool or application permission layer. Managed ALB/CDN choices may cover some needs differently.

PgBouncer pools PostgreSQL connections. Its pooling mode changes how long a client is associated with a server connection. Transaction pooling can conflict with assumptions about session state or certain prepared-statement/client behaviors unless the selected versions/configuration support them.

Add either tool for a measured boundary. A proxy timeout, app timeout, and provider timeout should form a coherent budget. A pool should protect capacity, not hide long transactions forever. Verify Rails/pg compatibility with the chosen mode in a separate test environment.''',
 '''```text
HTTP: browser → Nginx/ALB → Puma → Rails
SQL: Rails pool → PgBouncer (chosen mode) → PostgreSQL
```

For debugging, record which layer generated an error and whether a request/connection reached the next hop. A 504 and a DB pool checkout timeout are not the same symptom.''',
 '''Follow HTTP headers/body/timeouts through the proxy, then follow one database transaction through both client and server pools. Count application processes/pools and observe queued versus active DB work.

Test a feature relying on connection/session state before selecting transaction pooling. Do not infer compatibility from one simple SELECT.''',
 'Adding more pools can create more waiting layers. A proxy can buffer or time out large requests differently from the app. Session assumptions can break under a different pooling mode.',
 'A Rails feature uses session-level DB state and breaks after transaction pooling. What should be investigated?',
 'Identify the exact session-state/prepared-statement assumption, client/pg/PgBouncer versions, and selected pooling mode. Choose a compatible mode/configuration or remove the assumption with tests. Do not treat pooling as transparent in every case.',
 'A 60-second app operation sits behind a 30-second proxy timeout. What options should the product consider?',
 'Define an overall latency budget and whether the operation should be asynchronous. If synchronous behavior is required, align bounds deliberately and handle unknown outcomes. Do not just increase every timeout without capacity analysis.',
 [q('Nginx and PgBouncer primarily front which protocols?','HTTP and PostgreSQL respectively','Both only Kafka','Both only browser storage',0,'They solve different traffic boundaries.'),q('Is transaction pooling transparent to every session assumption?','Always','No','Only with Rails',1,'Session affinity/state behavior can change.'),q('What should justify another proxy/pool?','A concrete measured need and compatible contract','Its popularity alone','A bigger diagram',0,'Each added layer also adds failure and operating work.')],
 'Name the protocol and the waiting layer.', ['HTTP proxy','App server','Rails connection pool','DB pool mode','PostgreSQL transaction'], [('Nginx proxy guide','https://nginx.org/en/docs/http/ngx_http_proxy_module.html'),('PgBouncer features','https://www.pgbouncer.org/features.html')],usecase='Understanding existing reverse-proxy and DB pool deployments.',benefits='Traffic control and connection reuse where appropriate.',drawbacks='Timeout/buffering/session contracts can change behavior.',tags=['nginx','pgbouncer','performance'])

chapter('ops','metrics-stack','Prometheus and Grafana: collect a signal, then ask a question','beginner',
 'Explain metric collection, labels, rates, dashboards, and alert ownership without treating a graph as evidence by itself.',
 '''Prometheus commonly scrapes exposed metrics and stores time series. Grafana can query/display data from selected sources. A dashboard is a view over a data contract, not an independent guarantee that the service is healthy.

Counters accumulate events; rates describe change over time. Gauges describe a current value. Histograms can help examine latency distributions under their configuration. Choose labels with bounded categories. A ticket ID per metric label can create an enormous number of series.

Setup: define one task-relevant metric, expose it safely in a training service, configure a scrape, create a query/panel, and trigger a synthetic failure. Then write an alert with an owner and runbook. Consider hosted alternatives or Datadog when their operating model fits better; using both stacks is not mandatory.''',
 '''```text
completed_jobs_total{service="reporting", outcome="success"}
pending_jobs{service="reporting"}
oldest_pending_age_seconds{service="reporting"}
```

Use event IDs in appropriate logs/traces, not as a new time-series label for every event. Compare rate and age with failure/retry signals.''',
 '''App records bounded metric → collector observes → query transforms over a time window → panel/alert presents it → investigator checks user outcome. A missing scrape and a true zero value are different things.

For a latency claim, ask which requests were included and whether errors/timeouts were excluded. A low median can coexist with painful tail latency.''',
 'A mean alone can hide a slow minority. Unbounded labels can overwhelm the system. A pretty dashboard with no action/owner can fail silently during an incident.',
 'The dashboard says zero failures because the exporter stopped. Repair the interpretation and alerting.',
 'Monitor collection health/absence separately from application values. Distinguish missing data from zero. Test a stopped exporter and a real synthetic failure, and keep a user-level success/progress signal.',
 'A graph improves after slow requests are dropped from the metric. What denominator question matters?',
 'Define the measured population, outcome classes, and time window. Include or separately track timeouts/errors. Do not compare rates/latencies after silently changing inclusion rules.',
 [q('What is a counter rate useful for?','Events per time over a defined window','A single record’s permission','A secret value',0,'Rates make cumulative counters interpretable over time.'),q('Missing telemetry equals zero failures?','Yes','No','Only in Grafana',1,'Collection absence is a different state.'),q('Which label is usually bounded?','Outcome category','Every ticket UUID','Every raw URL query',0,'Bounded categories keep series growth manageable.')],
 'A graph is only as honest as its population and labels.', ['Metric contract','Collection','Windowed query','Dashboard or alert','Task-level verification'], [('Prometheus metric types','https://prometheus.io/docs/concepts/metric_types/'),('Grafana data sources','https://grafana.com/docs/grafana/latest/datasources/')],usecase='Open observability stacks and interpreting operational dashboards.',benefits='Flexible metric queries and shared operational views.',drawbacks='Collection, cardinality, retention, and alerting need operation.',tags=['prometheus','grafana','observability'])

chapter('ops','feature-flags','Feature flags: release control without permanent branching','intermediate',
 'Use a flag to limit exposure and define defaults, ownership, removal, and data compatibility.',
 '''A feature flag changes which behavior is active for a context. It can separate deployment from exposure and help a controlled rollout. It does not undo data already written or remove the need to test both paths.

Define the flag owner, intended lifetime, targeting inputs, safe default, and removal plan. Evaluate permissions on the server regardless of a client flag. A client-visible flag is not a secret access gate.

A flag provider is another dependency. Decide whether evaluation is local/cached/remote and what happens when it is unavailable. Keep the old/new schema compatible during overlap. Avoid combining many flags into untested state combinations.''',
 '''```text
Flag: new_ticket_assignment
Owner: ticket workflow team
Default on evaluation failure: old tested path
Target: training/internal cohort first
Guardrails: wrong assignments, error rate, lost drafts
Removal: after verified rollout and rollback window
```

The provider could be a managed flag platform or a small internal mechanism. Choose it from required targeting/audit/lifecycle needs.''',
 '''Request context → flag decision → chosen behavior → observable outcome → guarded expansion → retire old path. Log a bounded variant tag where useful so errors can be compared.

Rehearse disabling the flag after the new path has written data. If the old path cannot read that data, the flag is not an effective rollback.''',
 'A flag can become permanent dead code. A frontend flag does not authorize a server action. Untested combinations can multiply behavior states.',
 'The team calls a flag a rollback, but old code cannot read new records. Repair the release plan.',
 'Make the data contract backward compatible or provide a deliberate migration/recovery path. Test toggling after writes. A control over exposure is not a reversal of data effects.',
 'The flag provider is unavailable. What should be documented and tested?',
 'Evaluation mode/cache lifetime, safe default, stale targeting behavior, and whether the core action may continue. Keep server access checks independent. Test failure under the actual client/library contract.',
 [q('A flag undoes all data effects?','Yes','No','Only when off',1,'It controls behavior selection, not arbitrary historical writes.'),q('What should every temporary flag have?','Owner and removal plan','Only a catchy name','Only a frontend boolean',0,'Lifecycle prevents permanent accidental complexity.'),q('Can a client flag replace server permission?','Yes','No','Only for internal users',1,'Client state is not authority.')],
 'Deploy code. Control exposure. Retire the switch.', ['Owned flag','Context and safe default','Chosen path','Outcome guardrails','Removal or recovery'], [('OpenFeature concepts','https://openfeature.dev/docs/category/concepts/')],usecase='Controlled rollout of a risky workflow change.',benefits='Smaller exposure and deliberate rollback decisions.',drawbacks='State combinations, provider failure, and stale flags add complexity.',tags=['feature-flags','delivery'])

chapter('ops','toolkit-capstone','Choose the tools, then debug the whole application','intermediate',
 'Explain a production tool map and recover a synthetic incident without adding every tool by default.',
 '''A production architecture is a set of responsibilities. Packaging, orchestration, storage, messaging, observation, delivery, scheduling, and product analytics are different jobs. Several products can cover overlapping parts. Choose a coherent minimum and justify each additional tool.

For the support app, Docker packages; Compose runs the local lab; ECS or Kubernetes orchestrates; PostgreSQL owns business data; Redis may cache; Kafka carries retained events; Debezium can replace the polling outbox publisher; observability helps investigate; SendGrid/Pendo are optional external integrations with different data policies.

Practice one incident: reports are late, database connections are full, and users repeatedly click Export. Trace the oldest pending work, retries, DB waits, provider latency, and UI status. A full diagram is useful only if you can follow one item through it.''',
 '''```text
Delivery: Git → CI → image digest → chosen orchestrator
Request: edge/proxy → Rails → PostgreSQL → response
Async: outbox → Kafka → inbox/projection
Cache: scoped Redis copy → bounded fallback
Observation: OTel/Datadog or chosen metrics/log stack
Product: confirmed outcome → minimal analytics event
```

Write an alternative design with fewer tools and explain which requirements it still meets. Cassandra, Kubernetes, and Debezium are options, not badges.''',
 '''Begin at user impact. Identify the authority and each queued/retained copy. Find the oldest uncompleted item and its event/run ID. Distinguish delivery, processing, and UI problems. Repair the smallest broken boundary and verify both backlog recovery and user-visible completion.

Finish the cumulative toolkit quiz, then explain why a plausible alternative tool is a poor fit for three scenarios. Selection reasoning matters more than logo recognition.''',
 'Adding capacity to a poison-message loop can worsen the DB incident. Installing every monitoring stack can duplicate cost without improving a question. Product analytics cannot substitute for a durable business audit trail.',
 'A team proposes Cassandra and Kubernetes to fix a missing SQL index and a stale Vue response. Give a boundary-based repair.',
 'Measure the actual query and add a justified SQL/data-boundary repair; fix the frontend request owner/acceptance guard. Neither symptom alone requires a new database or orchestrator. State evidence and retest the original task.',
 'The polling dispatcher is replaced by Debezium. Which application contracts should remain stable?',
 'The committed outbox event identity/schema/key, duplicate-safe consumer effect, traceability, and recovery policy. Publishing machinery changes; business meaning and authority rules should remain deliberate. Test cutover duplicates and missing events.',
 [q('What should justify each tool?','A responsibility and requirement it serves','The number of logos','Popularity alone',0,'Every tool adds an operating contract.'),q('Where should incident diagnosis start?','User impact and the oldest incomplete work','The newest dashboard theme','A random restart of everything',0,'Trace a meaningful symptom through boundaries.'),q('What stays important when changing publisher technology?','Event identity/schema and consumer correctness','Only the vendor name','Only the container tag',0,'Transport changes do not erase business contracts.')],
 'Choose fewer tools well. Trace one item completely.', ['Requirement and tool role','Authoritative state','Async and cached copies','Correlated incident','Verified repair'], [('CNCF landscape context','https://landscape.cncf.io/'),('OpenTelemetry concepts','https://opentelemetry.io/docs/concepts/')],usecase='An end-of-course tool selection and incident exercise.',benefits='Connects tools to responsibilities and practical diagnosis.',drawbacks='A reference architecture is not a requirement to deploy every part.',tags=['capstone','architecture','tools'])
chapter('events','logs-queues','Events, commands, queues, and a retained log','beginner',
 'Choose messaging from responsibility, history, replay, and timing needs.',
 '''A command asks someone to do something: GenerateReport. An event states a fact: TicketCompleted. Naming the difference helps decide who owns rejection, completion, and follow-up work.

A work queue commonly distributes work among competing workers. A retained log keeps ordered records under a retention policy while each consumer group tracks its own progress. Kafka is useful for independent subscribers and replay, not merely because a system has background jobs.

Asynchronous communication moves a boundary in time. It can buffer work and decouple processing, but users need an honest pending/result model. It also adds duplicates, schema evolution, delayed access/context, and operational recovery questions. A direct call or existing job queue can be simpler when those benefits are not needed.''',
 '''```text
Command: GenerateReport(report_run_id)
Owner: reporting worker; outcome ready/failed.

Event: TicketCompleted(event_id, ticket_id, workspace_id, version)
Subscribers: reporting projection and notification intent.
Each subscriber has independent progress and failure handling.
```

Do not use an event name to hide a synchronous business requirement. If completing the ticket requires another decision now, model that dependency explicitly.''',
 '''Business decision commits → fact is published → independent subscribers process later → their results become visible. Ask where a user can check each outcome and how old work may be replayed.

Compare one reporting group with three workers versus two independent groups. Worker count and subscriber responsibility are different axes.''',
 'Changing a direct call into an event does not make the effect immediate or atomic. A queue/log is not the application’s permission authority.',
 'The app needs one export worker and no replay/independent subscribers. The team adds Kafka by default. Assess the choice.',
 'Compare an existing durable job queue or SQS with Kafka’s retained-log benefits and operational cost. Choose Kafka only if independent event consumers/replay/stream requirements justify it. Keep idempotence and outcome tracking either way.',
 'A new analytics subscriber needs the last month of ticket facts. What requirement now matters?',
 'Retained replayable history or a deliberate backfill source, a stable schema, independent progress, and privacy/retention policy. Verify the available retention window before promising recovery.',
 [q('Which name expresses a fact?','TicketCompleted','GenerateReport','SendEmailNow',0,'Past-tense facts and requested actions carry different responsibility.'),q('What does each Kafka consumer group track?','Its own progress','Only the producer’s RAM','One global deleted-message flag',0,'Independent groups can process the retained log separately.'),q('Is Kafka required for every background job?','Yes','No','Only for Rails',1,'Choose from actual history/subscriber/throughput needs.')],
 'Command asks. Event tells. Log remembers under a policy.', ['Business decision','Command or fact','Queue or retained log','Independent processing','Visible outcome'], [('Kafka introduction',KAFKA+'getting-started/introduction/')],usecase='Choosing a messaging model for reports and ticket facts.',benefits='Clear responsibility and justified asynchronous boundaries.',drawbacks='Async systems need duplicate, delay, schema, and recovery handling.',tags=['kafka','messaging','fundamentals'])

chapter('events','partitions','Topics, partitions, keys, and local order','beginner',
 'Predict record placement and explain the scope and limits of ordering.',
 '''A Kafka topic is split into partitions. Each partition is an ordered append log with offsets. Offset 10 in partition 0 is unrelated to offset 10 in partition 1; it is not a global event number.

A record key helps the partitioner place related records together under a stable configuration. Using ticket identity as the key can keep that ticket’s records on one partition. It does not order all tickets globally. A single very hot key can limit useful parallelism.

Adding partitions can change key-to-partition mapping. If per-entity ordering matters across such a change, plan migration/transition semantics rather than assuming the old placement stays unchanged. Also keep application version/sequence checks when events can be retried or produced through several paths.''',
 '''```text
Topic ticket-events
Partition 0: offset 0 [ticket A v1], offset 1 [ticket A v2]
Partition 1: offset 0 [ticket B v1]

Key = workspace_id + ticket_id under a deliberate stable contract.
Value = versioned event envelope.
```

Consumer parallelism is constrained by partition assignment within a group. Adding more consumers than active partitions does not give every member a partition.''',
 '''Producer chooses key → partitioner selects partition → leader appends record → offset identifies its position → assigned consumer processes that partition. Two partitions can advance at different speeds.

Draw A1/A2 in one partition and B1/B2 in another. There is no single cross-partition order you can infer merely from their offsets.''',
 'A key is not a global lock. A large number of partitions is not free operationally. Changing keys can scatter one entity’s history.',
 'A service compares offsets from different partitions to decide the latest ticket update. Repair the version rule.',
 'Use per-entity business versions/timestamps under a defined contract and preserve the key/partition ordering strategy. Offsets only order positions within a partition. Test delayed/stale entity updates and partition-count changes.',
 'One workspace dominates traffic under a workspace-only key. What tradeoff should be considered?',
 'Choose the smallest key scope that satisfies the required ordering, perhaps ticket identity rather than all workspace traffic. This increases parallelism but removes workspace-global order. Define that requirement before changing the key.',
 [q('Offsets from different partitions are a global order?','Yes','No','Only when equal',1,'Each partition has its own position space.'),q('More consumers than partitions in one group means what?','Some may be idle for that topic','Every consumer gets every record','Automatic global order',0,'Assignment bounds active parallelism.'),q('A hot single key can do what?','Limit one partition’s throughput','Spread itself evenly automatically','Remove all retries',0,'Related records placed together can create skew.')],
 'Order lives inside a partition, not in the topic name.', ['Record key','Partition choice','Leader append','Partition offset','Assigned consumer'], [('Kafka concepts',KAFKA+'getting-started/introduction/'),('Kafka design',KAFKA+'design/design/')],usecase='Ordered ticket state and scalable subscriber work.',benefits='Predictable local order and controlled partitioning.',drawbacks='Hot keys and repartitioning complicate scaling.',tags=['kafka','partitions'])

chapter('events','layers','Kafka layers: clients, brokers, storage, replicas, controllers','beginner',
 'Follow one record through discovery, batching, append storage, replication, and consumer fetch.',
 '''The client library handles protocol requests, metadata, batching, retries, and serialization integration. A bootstrap address helps discover the cluster. The client then communicates with relevant broker endpoints; bootstrap is not a permanent universal proxy.

Brokers host partition leaders/replicas and serve produce/fetch requests. Records are stored in log segments with indexes; the operating system page cache and sequential I/O are part of the performance picture. This is a useful layer model, not a need to memorize every disk-file suffix.

Controllers manage cluster metadata/leadership under the selected Kafka mode. The course lab uses Kafka 4.1 KRaft, not a ZooKeeper tutorial. Replica placement and acknowledgement policy decide which failures an accepted record should survive. A one-broker local lab cannot demonstrate multi-broker availability.''',
 '''```text
Rails → Ruby client → metadata discovery → partition leader
                           producer batch → replicated append
Reporting client ← fetch records ← partition log
KRaft controller quorum → cluster metadata/leadership
```

Distinguish data-plane record traffic from control-plane metadata decisions. A controller outage and a consumer bug are different failure classes.''',
 '''The producer discovers leader endpoints, sends a batch, and receives an acknowledgement under its configuration. A consumer fetches retained records from assigned partitions. It does not require the producer process to remain alive after durable publication.

When a client cannot connect after initial discovery, inspect advertised listeners/DNS/network/auth for actual broker addresses. When append latency rises, inspect broker/storage/replica health rather than only Rails CPU.''',
 'One local broker hides replica/failover behavior. Acknowledgement settings cannot create replicas that do not exist. Confusing controller roles with business consumers makes diagnosis random.',
 'A local compose demo is described as “highly available production Kafka.” Correct the claim and the test plan.',
 'Label it a single-broker development setup with replication factor one. Explain that HA requires a deliberately configured multi-broker/controller design and failure tests. The demo proves client/event flow, not zone/broker survival.',
 'Producing is slow while Rails CPU is low. Which layers should you examine?',
 'Client queue/batching, network/TLS, broker request latency, storage pressure, and replica acknowledgement/ISR health. Measure the wait rather than assuming more app threads are the remedy.',
 [q('What is bootstrap mainly for?','Cluster metadata discovery','A universal DB transaction','A guarantee of all broker reachability',0,'Clients subsequently use discovered endpoints.'),q('What does the one-broker lab prove about HA?','No multi-broker survival guarantee','Full zone resilience','Three-replica durability',0,'Its topology cannot test missing replicas.'),q('What manages Kafka cluster metadata in this lab?','KRaft controllers','The Rails model callback','A Vue store',0,'Kafka 4.1 lab uses the KRaft mode.')],
 'Client → leader log → replicas; controller manages metadata.', ['Client library','Metadata and leader','Batched append','Replica acknowledgement','Consumer fetch'], [('Kafka implementation',KAFKA+'implementation/'),('Kafka KRaft',KAFKA+'getting-started/zk2kraft/')],usecase='Debugging Kafka by layer instead of treating it as one box.',benefits='A concrete model for network, storage, and coordination symptoms.',drawbacks='A local flow demo cannot certify production durability or performance.',tags=['kafka','architecture','fundamentals'])

chapter('events','producer','Producers: acknowledgements, idempotence, and duplicate business events','beginner',
 'Distinguish client retry deduplication from repeated application publication.',
 '''A producer serializes a record and asks a partition leader to append it. Its delivery handle/future reports the result under the client configuration. Enqueueing into a client buffer is not the same as an acknowledged broker append.

acks, replica/min-ISR settings, retry limits, and delivery timeouts interact. Idempotent producer support prevents certain retry duplicates under the protocol/session contract. It does not recognize that two separate application calls with different identities mean the same business completion.

Always carry a stable business event ID. In the outbox, retrying the same saved event preserves that ID. A consumer can then deduplicate the business effect even when the application re-publishes after a crash. Choose and verify settings for the actual client library; Ruby librdkafka options are not every Java default pasted unchanged.''',
 '''```ruby
producer = Rdkafka::Config.new(
  'bootstrap.servers' => ENV.fetch('KAFKA_BROKERS'),
  'enable.idempotence' => true,
  'acks' => 'all'
).producer
handle = producer.produce(topic: 'ticket-events',
  key: ticket_key, payload: JSON.generate(event_envelope))
handle.wait # publication result; not consumer completion
```

The tested lab supplies lifecycle/error handling. On a one-replica topic, acks=all still means only that configured replica set, not three-broker durability.''',
 '''Saved event E → client buffer → batch send → broker acknowledgement → mark outbox published. Crash after acknowledgement but before the DB mark means E may be published again.

The producer’s protocol identity does not make the DB mark and Kafka append one transaction. The consumer inbox is still needed for this gap.''',
 'Fire-and-forget publication can lose errors. Producer idempotence is often overclaimed as exactly-once business processing. App-level resends remain a distinct duplicate source.',
 'The dispatcher marks published immediately after calling produce without waiting. A broker failure loses delivery. Repair the boundary.',
 'Wait for the client’s delivery result under bounded configuration before marking publication. Keep stable event identity and retry unpublished intent. Still expect the ack-before-mark crash duplicate and handle it downstream.',
 'The same ticket completion is published twice by two app code paths. Does enable.idempotence solve that?',
 'No. Enforce one logical completion/outbox event at the authority boundary and use stable event IDs with consumer deduplication. Producer retry idempotence does not infer business sameness from two independent calls.',
 [q('Calling produce proves consumers finished?','Yes','No','Only with acks=all',1,'Producer acceptance/acknowledgement is not downstream completion.'),q('Producer idempotence deduplicates every app resend?','Yes','No','Only with JSON',1,'Its protocol scope differs from business identity.'),q('Why keep event_id on retries?','To identify the same logical fact downstream','To replace every offset','To authorize users',0,'Stable business identity supports repeat-safe processing.')],
 'Buffer accepted ≠ broker acknowledged ≠ business completed.', ['Stable event ID','Client buffer','Broker append and replicas','Delivery result','Outbox publication mark'], [('Kafka producer config',KAFKA+'configuration/producer-configs/'),('Ruby rdkafka client','https://github.com/karafka/rdkafka-ruby')],usecase='Reliable publication of saved Rails events.',benefits='Clear publication evidence and stable retry identity.',drawbacks='The DB/Kafka publication gap still permits repeats.',tags=['kafka','producer'],lab='rails-kafka')

chapter('events','consumers','Consumers: groups, positions, stored offsets, and commits','beginner',
 'Predict replay from the committed next offset and avoid acknowledging unfinished work.',
 '''A consumer group shares partition responsibility among its members. A different group has independent progress and can read the same retained records. Within a group, one assigned member normally owns a partition at a time under the selected group protocol.

Distinguish fetched position, a client’s stored progress, and committed group offsets. Exact APIs vary by library. A committed offset conventionally identifies the next record to resume from, not the last business event ID.

Process the durable effect before committing the relevant completed progress. A crash after effect but before commit replays it. Committing too early can skip unfinished work after a crash. Auto offset reset applies when there is no usable committed position; earliest does not rewind a healthy group on every restart.''',
 '''```text
Partition records: 0, 1, 2, 3
Completed durable effects: 0 and 1
Safe resume offset: 2

Crash after effect for 2, before commit:
resume at 2 → effect must tolerate repetition.
```

The lab uses a synchronous rdkafka message commit after its DB transaction and disables automatic commit/store behavior explicitly.''',
 '''Assigned partition → fetch → validate → DB transaction → commit completed progress. Parallel processing needs a contiguous completion frontier: do not commit past an earlier unfinished record merely because a later one finished.

Test a consumer restart with an existing group and then a new group. Explain the difference from resetting offsets deliberately.''',
 'A high fetched position does not mean business work completed. More group members than partitions can leave members idle. An automatic progress setting can acknowledge work before your code intended.',
 'Offset 11 finishes before offset 10 in a parallel consumer, and the client commits 12. What can be lost after crash?',
 'The unfinished effect for 10 can be skipped on resume. Track the contiguous completed frontier per partition or process serially per partition with a clear commit boundary. Test out-of-order completion and crash.',
 'A developer sets auto.offset.reset=earliest but the group resumes late in the topic. Why?',
 'The group has a usable committed offset, so reset fallback is not used. Inspect group progress. A deliberate replay needs a new group or a controlled offset reset with the correct consumer/effect policy.',
 [q('Committed offset 7 conventionally means resume where?','At the next record position 7','Always event_id 7','Before every record',0,'Offsets are partition positions; commit records a resume point.'),q('Earliest rewinds every restart?','Yes','No, only under reset conditions','Only with Ruby',1,'Existing usable group commits take precedence.'),q('Commit before durable effect risks what?','Skipping unfinished work after crash','Only duplicates','Automatic rollback',0,'The group may resume beyond work that never completed.')],
 'Fetch is not finish. Commit only completed progress.', ['Partition assignment','Fetched position','Durable effect','Contiguous completion','Committed resume offset'], [('Kafka consumer config',KAFKA+'configuration/consumer-configs/')],usecase='A reporting group with controlled replay.',benefits='Independent subscribers and explicit progress.',drawbacks='Incorrect offset handling can lose or duplicate business work.',tags=['kafka','consumer'],lab='rails-kafka')

chapter('events','schemas','Event envelopes, evolution, and privacy','beginner',
 'Define event identity, entity key, business version, time, and a compatible payload contract.',
 '''An event envelope makes meaning explicit. Include event_id, event_type, schema_version, aggregate identity/version, occurred_at, and minimal payload. Distinguish when the business fact happened from when a consumer processed it.

Do not publish an entire Rails model by habit. It couples consumers to private columns and may expose data they do not need. Use the smallest fact that supports the subscriber’s job. A schema registry can help manage format compatibility; it does not decide business meaning or permission policy for you.

For evolution, add optional fields with clear defaults where compatible. Renaming/removing a required field can break old consumers. Producers and consumers may run different versions during deployment. Test representative old/new messages, not only the newest example.''',
 '''```json
{
  "event_id":"synthetic-e1","event_type":"TicketCompleted",
  "schema_version":1,"aggregate_id":"42","aggregate_version":3,
  "workspace_id":"7","occurred_at":"2026-10-21T09:00:00Z",
  "data":{"title":"Synthetic ticket"}
}
```

This is teaching data. The lab validates required fields and refuses unsupported schema versions. It does not serialize the work project’s models.''',
 '''Business fact → envelope builder → serialization → broker bytes → consumer parsing → schema/business validation → effect. A valid JSON document can still be an invalid event.

For a new optional field, test an old consumer ignoring it and a new consumer handling its absence. For a new event meaning, choose a deliberate version/type transition rather than silently repurposing a field.''',
 'Changing the same field’s meaning without changing the contract can create correct-looking wrong reports. Personal/free text can spread to every subscriber and retained log.',
 'A producer publishes ticket.attributes and consumers start depending on internal flags. Redesign the event.',
 'Define a minimal stable fact/envelope, document field meaning and access/retention, and migrate consumers deliberately. Keep event ID and aggregate version separate. Test old/new schema compatibility and reject malformed required data.',
 'A new consumer receives an unsupported schema version. What should happen?',
 'Use an explicit failure/quarantine/retry policy with diagnostics and owner; do not commit past required work silently. Deploy compatible support or route to a deliberate recovery path, then replay safely.',
 [q('Valid JSON proves a valid event contract?','Yes','No','Only with an event_id',1,'Shape, version, and meaning still need validation.'),q('What should payload scope follow?','Subscriber need and data policy','Every model column','The largest object available',0,'Minimal contracts reduce coupling and exposure.'),q('Event ID and aggregate version are the same thing?','Yes','No','Only for one partition',1,'One identifies a fact; the other orders entity state under a contract.')],
 'Identity, meaning, version, time, and minimal data.', ['Business fact','Versioned envelope','Serialized record','Validated consumer input','Compatible effect'], [('CloudEvents concepts','https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md'),('Kafka serialization context',KAFKA+'getting-started/introduction/')],usecase='Long-lived event contracts across teams/releases.',benefits='Less coupling and clearer replay/debugging.',drawbacks='Compatibility, retention, and private-data scope require governance.',tags=['kafka','schemas','contracts'],lab='rails-kafka')

chapter('events','outbox','Rails transactional outbox: save intent with the change','intermediate',
 'Close the DB/publish loss gap while accepting and handling duplicate publication.',
 '''A direct DB write followed by a Kafka send is a dual write. Crash after DB commit but before send loses the event. Send first and a later DB rollback can publish a fact that never committed. Neither ordering solves both cases.

An outbox stores the business change and event intent in one PostgreSQL transaction. A separate dispatcher publishes committed rows. If it crashes after Kafka acknowledgement but before marking the row published, it may resend the same event. The outbox trades lost intent for a repeatable delivery path; it does not create universal exactly-once effects.

Keep a stable event ID and a unique business rule for creating the completion fact. Define dispatcher concurrency and ordering. The lab starts with one serial dispatcher for clarity; a production multi-worker design needs claim leases/locking, throughput, ordering, and stuck-work recovery.''',
 '''```ruby
Ticket.transaction do
  ticket.lock!
  unless ticket.completed?
    ticket.update!(status: 'completed', version: ticket.version + 1)
    OutboxEvent.create!(event_id: SecureRandom.uuid,
      aggregate_id: ticket.id.to_s,
      envelope: build_completed_event(ticket))
  end
end
```

The runnable lab defines every model/migration/service and keeps this transaction local. No network call is made while holding the ticket lock.''',
 '''HTTP completion → lock/check → ticket update + outbox insert → DB commit → dispatcher reads → producer delivery acknowledgement → published mark. Break the process at each arrow and state what can be retried.

after_commit enqueue alone still has a crash gap. It can be useful as a wake-up, but a durable scanner/outbox source must recover missing wake-ups.''',
 'Holding a DB lock during a slow network send can hurt capacity. Multiple dispatchers can reorder or duplicate without a deliberate claim strategy. A published flag is evidence of a local mark, not downstream completion.',
 'A callback publishes directly before commit, and reporting sees a rolled-back completion. Repair the fact boundary.',
 'Save the event intent with the state change in the DB transaction. Publish only committed outbox rows later. Keep stable IDs and duplicate-safe consumers. Test rollback leaves neither completion nor outbox event.',
 'The dispatcher sends E successfully then crashes before updating published_at. What should happen next?',
 'It can resend E under the same event_id. The consumer must deduplicate its effect transactionally. Do not mark first to avoid duplicates, because that reintroduces lost delivery.',
 [q('What does the outbox make atomic?','Business DB change and saved event intent','PostgreSQL plus every remote effect','Every consumer offset',0,'It is a local DB transaction boundary.'),q('Can an acknowledged event be resent after dispatcher crash?','Yes','No','Only without JSON',0,'The published mark is a separate write.'),q('Should a slow network call hold the business row lock by default?','Yes','No, separate it when semantics permit','Only in Rails',1,'Keep the transaction/lock window bounded.')],
 'Commit the fact and its intent together. Publish later. Expect repeats.', ['Trusted completion command','Ticket lock and rule','State plus outbox commit','Acknowledged publication','Published mark or resend'], [('Transactional outbox context','https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html')],usecase='Reliable Rails facts consumed by other services.',benefits='No lost publication intent after a committed business change.',drawbacks='Dispatcher operations and duplicate handling remain.',tags=['rails','outbox','kafka'],lab='rails-kafka')

chapter('events','inbox','Consumer inbox: one local effect for a repeated event','intermediate',
 'Commit deduplication and projection changes together, then acknowledge Kafka progress.',
 '''A consumer can receive a record again after a crash/rebalance/replay. A seen? query followed by a write races when two processes overlap. Use a unique consumer-specific event key at the authority that stores the effect.

An inbox row and projection update in one DB transaction make the local effect repeat-safe: either both commit or neither does. A later Kafka offset commit remains a separate step. If that commit fails, replay checks the inbox and avoids repeating the local projection.

This does not atomically include email, another database, or every external API. Each side-effect boundary needs its own intent/idempotency/reconciliation design. “Exactly once” must name the scope where it is enforced.''',
 '''```text
DB transaction:
  INSERT inbox (consumer_name, event_id) under unique constraint
  if new: update reporting projection
  commit
After DB transaction: commit Kafka message progress

On duplicate: skip the already committed local effect,
then allow progress acknowledgement.
```

For PostgreSQL, catch a uniqueness exception outside the failed transaction before starting further SQL; a statement error can leave that transaction aborted.''',
 '''Receive E → validate → insert inbox + update report → commit DB → commit Kafka. Crash after DB commit before Kafka commit: receive E again → unique inbox says local effect exists → do not repeat it → commit progress.

Include consumer identity in deduplication scope when different projections independently need the same event. Their completion responsibilities are separate.''',
 'Writing inbox before the effect in a separate committed transaction can lose the effect. Writing it after can duplicate. A memory Set disappears on process restart.',
 'The consumer marks an event seen, commits, then crashes before updating the report. Repair the transaction.',
 'Store inbox/dedup and the local report effect in the same DB transaction, protected by a unique key. Commit Kafka only afterward. Test failure after inbox insert and before effect so both roll back.',
 'The same event should update reporting and notification intent independently. What should dedup scope be?',
 'Use separate consumer/effect identities or separate inbox tables. A global seen flag must not cause one subscriber to skip its required effect because another subscriber processed the event.',
 [q('What must share the inbox transaction?','The local business/projection effect','Every remote service in the world','Only a log line',0,'Atomic local dedup prevents a lost or repeated local effect.'),q('A pre-check without a unique constraint can do what?','Race','Guarantee uniqueness','Replace the transaction',0,'Two clients can both see absent.'),q('Crash after DB commit before offset commit causes what?','Replay that should be deduplicated','Automatic DB rollback','Guaranteed event loss',0,'The committed inbox makes the local replay safe.')],
 'Dedup plus local effect together. Offset after.', ['Validated event','Unique consumer inbox','Projection transaction','DB commit','Kafka acknowledgement'], [('Kafka consumer contract',KAFKA+'configuration/consumer-configs/'),('PostgreSQL transactions','https://www.postgresql.org/docs/current/tutorial-transactions.html')],usecase='Reporting/search/materialized projections.',benefits='Repeat-safe local effects across process crashes.',drawbacks='External side effects need additional boundaries.',tags=['kafka','inbox','idempotency'],lab='rails-kafka')

chapter('events','retries','Retries, poison events, and the ordering tradeoff','intermediate',
 'Choose blocking retry, retry topics, or quarantine from the required per-entity behavior.',
 '''A transient outage and an invalid schema are different failures. Retrying malformed data forever does not repair it. Classify failures, bound attempts/delay, and retain enough safe context for diagnosis.

Blocking a partition preserves its processing order but can hold back unrelated keys there. Sending a failed item to a retry topic lets later records advance, which can reorder one entity’s effects. A dead-letter/quarantine path needs ownership, alerting, retention, and redrive rules; it is not a successful business outcome.

Never commit past required work silently. If the product permits skipping/quarantine, record that decision durably and explain the resulting projection completeness. Replays must remain idempotent and schema-compatible.''',
 '''```text
Failure categories
temporary DB outage → bounded retry/backoff, retain position
invalid event schema → visible stop/quarantine under policy
business stale version → deliberate ignore/reconcile rule
unknown remote side effect → reconcile, not blind resend
```

The lab deliberately stops on invalid input and leaves the offset uncommitted. Retry/DLQ routing is a follow-up design exercise, not silently implemented magic.''',
 '''Receive A1 → fails → choose policy → observe whether A2/B1 may proceed → repair → redrive A1 → verify entity/projection version. Draw the order after every proposed retry design.

Use event_id, key, schema version, topic/partition/offset, attempt, and safe error category in diagnostics. Keep sensitive payloads out of logs.''',
 'Retry topics can break per-key ordering if not designed for it. A DLQ can become a graveyard. More workers do not solve a deterministic poison message.',
 'A1 is delayed to a retry topic, A2 applies first, then A1 overwrites the new state. Repair the version/order rule.',
 'Enforce per-entity versions/transition rules or preserve required order through a deliberate partition/key retry strategy. Distinguish state replacement from additive events. Test delayed A1 after A2 and define reconciliation rather than blind overwrite.',
 'An invalid event blocks a busy partition. What must the team decide?',
 'Whether to block for correctness or durably quarantine/skip under an accepted completeness policy. Establish owner, alert, repair/redrive, and ordering effects. Do not silently commit and call it success.',
 [q('Does retrying malformed JSON usually fix it?','Yes','No','Only with more consumers',1,'Classify deterministic poison separately from transient failure.'),q('Retry topics can change what?','Per-entity processing order','Only CSS state','Database engine version',0,'Later records can pass a delayed failed item.'),q('A DLQ means what?','A recovery responsibility remains','The effect completed','No monitoring is needed',0,'Quarantine needs a repair/redrive process.')],
 'Every retry design is also an ordering design.', ['Classify failure','Choose delay/block/quarantine','Preserve required rule','Repair and redrive','Verify completeness'], [('Kafka operations',KAFKA+'operations/operations/')],usecase='A consumer that must remain correct during outages and bad input.',benefits='Explicit recovery instead of infinite or silent failure.',drawbacks='Progress, ordering, and completeness can trade off.',tags=['kafka','retry','operations'])

chapter('events','operations','Lag, rebalances, retention, and the debugging checklist','intermediate',
 'Diagnose slow or missing processing from broker, group, DB, and event identity evidence.',
 '''Lag is a progress difference, not a complete user-impact measure. A small lag can contain very old important work; a large lag can drain quickly. Observe oldest unprocessed age, processing rate, errors/retries, and backlog growth as well.

Group membership changes and poll/processing behavior can trigger rebalances. An assignment change means a new process may own a partition and replay uncommitted work. Long processing, insufficient polling, and uncontrolled parallelism can interact with the client’s liveness contract.

Retention limits available history. A consumer offline beyond it needs a rebuild/backfill source. Compaction is a different policy from keeping every event forever: key/tombstone/latest-value behavior must fit the topic’s purpose. The lab uses delete-retained event history for clarity.''',
 '''```sh
# Inside the lab Kafka container:
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
  --describe --group ticket-reporting-v1
/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 \
  --describe --topic ticket-events
```

Use the exact lab group/topic names. Read commands before using them in any other cluster. Offset reset is a deliberate mutation, not a first diagnostic.''',
 '''Missing report → locate outbox event → publication result → topic/partition record → group committed progress → inbox row → projection. The first missing boundary narrows the investigation.

For slow work, compare producer rate, consumer processing time, DB wait, hot partitions, and rebalance frequency. Adding partitions/consumers changes contracts and is not always the smallest repair.''',
 'A group may be subscribed to the wrong topic or have a different ID. earliest does not rewind existing commits. Resetting offsets can repeat external effects.',
 'Lag rises while consumer logs show repeated rebalances. What should be investigated?',
 'Processing/poll interval, batch size/concurrency, client liveness configuration, crashes/resource pressure, and membership churn. Protect effect/offset correctness first, then tune measured bounds. Do not just increase timeouts without knowing the work duration.',
 'The event is in Kafka but there is no inbox row. Which boundaries remain?',
 'Check group/topic assignment and committed position, parsing/schema failure, consumer logs/process health, and DB transaction failure. Kafka presence proves publication, not consumption or business completion.',
 [q('Lag alone fully describes user impact?','Yes','No','Only with three partitions',1,'Age, rate, errors, and importance matter.'),q('What can a rebalance lead to?','A new owner replaying uncommitted work','Automatic business rollback','Global order across topics',0,'Ownership and committed progress determine replay.'),q('What is a good first offset investigation?','Describe group progress before resetting it','Reset every group immediately','Delete retained data',0,'Observe before mutating recovery state.')],
 'Outbox → record → group → inbox → projection.', ['Event identity','Broker record','Group progress','Consumer transaction','Projection and age'], [('Kafka operations',KAFKA+'operations/operations/'),('Consumer settings',KAFKA+'configuration/consumer-configs/')],usecase='Debugging the real reporting path.',benefits='A repeatable boundary-based investigation.',drawbacks='Metrics and retained history have limits; reset/replay can affect business effects.',tags=['kafka','debugging','operations'],lab='rails-kafka')

chapter('events','rails-lab','Read the Rails/Kafka app one file at a time','intermediate',
 'Run and explain the complete multi-file path from HTTP completion to a repeat-safe reporting projection.',
 '''The local lab uses fresh support-ticket code. It borrows broad production patterns—service objects, transactions, workers, and projections—without copying private application code or data. It uses Ruby 3.3/Rails 7.2 with a pinned Kafka client; that is separate from the Ruby 2.7/Rails 4.2 work baseline.

Read in this order: routes/controller, CompleteTicket service, migrations/models, envelope builder, Kafka producer adapter, outbox dispatcher, reporting projector, consumer loop, and tests. Each file owns one boundary. Infrastructure/config files explain how the processes find one another.

Run the smoke script and failure drills with synthetic data. Do not merely watch logs scroll. Predict the ticket, outbox, topic, inbox, and projection state at each stop point. The app contains no real email, analytics, or cloud credentials.''',
 '''```text
POST /tickets/:id/complete
  → CompleteTicket.call
  → transaction(ticket + outbox)
  → OutboxDispatcher
  → KafkaPublisher delivery acknowledgement
  → ReportingConsumer
  → transaction(inbox + projection)
  → commit message offset
```

Open the app’s Hands-on lab tab for the complete file tree and commands. The README includes expected observations, repeat-event checks, and safe cleanup limited to this Compose project.''',
 '''Create one synthetic ticket. Complete it twice: the business transition should create one logical completion event. Wait for reporting: one inbox/effect appears. Re-publish the saved envelope: Kafka can contain another record with the same event_id, while the local projection effect remains one.

Stop the dispatcher before completion, then restart it. Saved intent should still be found. Stop the consumer, publish, then restart it. Retained history and group progress should let it catch up within retention.''',
 'The lab is intentionally one broker and one serial dispatcher. It does not prove multi-zone HA, high-throughput ordering under several dispatchers, production auth, or every legacy-fork behavior.',
 'A learner sees a committed ticket and outbox row but no report. Use the file map to locate the first broken boundary.',
 'Check unpublished outbox state/dispatcher logs, producer acknowledgement, broker record, consumer group/topic, schema errors, inbox transaction, and projection. Keep event_id through every step. Change one boundary and rerun the smallest check.',
 'How would you adapt the design to the work stack without copying this lab’s Gemfile?',
 'Keep the use-case/outbox/inbox contracts, then verify legacy migration syntax, JSON column support, lock/transaction behavior, autoload paths, and a Ruby-2.7-compatible Kafka client in an isolated authorized environment. Current lab dependencies require a different runtime.',
 [q('Does the lab run inside the work project?','No, it is a separate synthetic app','Yes, it changes its gems','Only its production DB',0,'The private project stays read-only.'),q('What should duplicate envelope publication do locally?','Keep one inbox/projection effect','Double the business effect','Erase Kafka history',0,'Business deduplication is independent of record count.'),q('What does the one-broker lab not prove?','Production HA','A local event flow','The tested DB transaction contract',0,'Its topology cannot demonstrate multi-broker survival.')],
 'One file, one boundary, one observable state.', ['HTTP service','DB outbox','Kafka adapter','Consumer inbox','Reporting projection'], [('Pinned Ruby Kafka client','https://github.com/karafka/rdkafka-ruby/tree/v0.20.0'),('Kafka 4.1 quickstart',KAFKA+'getting-started/quickstart/')],usecase='A hands-on end-to-end event application.',benefits='Turns abstract Kafka guarantees into inspectable files and failure drills.',drawbacks='A deliberately small local topology has documented production limits.',tags=['rails','kafka','lab'],lab='rails-kafka')

chapter('events','replay-capstone','Replay, rebuild, and explain the complete event system','intermediate',
 'Design a safe projection rebuild and explain which effects may and may not be replayed.',
 '''Replay is a tool for a purpose. Rebuilding a reporting projection from retained facts can be useful. Re-sending every email or charging every payment again is a different and often unacceptable effect. Separate rebuildable projections from irreversible side-effect workflows.

A new group gets independent progress, but an existing inbox for the same consumer identity may intentionally skip old event IDs. To rebuild, use a deliberately versioned projection/inbox identity or a controlled reset/migration plan. Keep the old projection available until the new one is verified when that is the chosen rollout.

State the recovery contract: authoritative source, available retention, schema compatibility, privacy/deletion policy, event ordering/version rules, and comparison checks. If facts have expired or were never published, offsets alone cannot rebuild them.''',
 '''```text
reporting-v1 → current projection and inbox
reporting-v2-rebuild → separate group + separate projection/inbox identity
Compare counts/state on a known synthetic dataset.
Switch reads deliberately after verification.
Do not invoke notification sending from the rebuild projector.
```

A schema change may require upcasting/translation of old events. Document the old contract rather than silently reading old bytes with new assumptions.''',
 '''Choose rebuild purpose → validate retained/backfill source → create isolated projection identity → replay → compare to authority/expected fixtures → switch reads → monitor → retire old state under retention policy.

For restore, draw the timeline of DB state, outbox marks, Kafka retained records, group commits, and inbox/projection state. Recovery is a reconciliation problem across those boundaries.''',
 'Resetting offsets while keeping the same inbox can result in no new projection writes. Clearing inbox blindly can repeat external effects. Old events may contain data that current privacy policy no longer permits retaining/replaying.',
 'A developer resets the group to earliest, but the report stays empty because all event IDs are marked seen. Repair the rebuild design.',
 'Use a new versioned projection/inbox identity or a controlled consistent rebuild of both, with clear read cutover and rollback. Verify old/new schema compatibility and retained history. Do not delete dedup state without understanding external effects.',
 'The DB restore predates some Kafka events and an email was already sent. What should recovery avoid?',
 'Avoid blindly replaying irreversible effects. Reconcile authoritative business state and delivery records using stable identities/status sources. Rebuild pure projections separately and record unknown outcomes. A Kafka transaction does not retroactively unify restored DB and external provider history.',
 [q('Should every side effect be replayed like a projection?','Yes','No','Only with a new group',1,'Irreversible effects need separate recovery semantics.'),q('Why can a fresh group still skip effects?','The same consumer inbox already marks IDs seen','Kafka deleted every record automatically','The event key is CSS',0,'Group progress and local deduplication are separate state.'),q('What must a rebuild verify?','Source history, schema, identity, ordering and comparison','Only process startup','Only a new topic name',0,'Recovery correctness crosses several boundaries.')],
 'Replay the facts for a purpose, not every side effect.', ['Rebuild purpose','Available facts','New projection identity','Replay and compare','Controlled read cutover'], [('Kafka design',KAFKA+'design/design/'),('Kafka group operations',KAFKA+'operations/operations/')],usecase='Projection evolution and disaster-recovery reasoning.',benefits='Makes replay a controlled engineering operation.',drawbacks='Missing history, privacy, and irreversible effects can limit recovery.',tags=['kafka','capstone','replay'],lab='rails-kafka')

chapter('frontend','functions-objects','JavaScript functions, closures, and object lookup','beginner',
 'Predict captured values, call-time this, and property lookup in everyday UI code.',
 '''A function can keep access to variables from the scope where it was created. That is a closure. It captures a binding, not always a frozen copy of the value. A later mutation can change what a callback reads. Each function call can also create a separate binding, which is why a factory can give each widget private state.

For a normal function, this depends on how it is called. obj.method() supplies obj. Taking const fn=obj.method and calling fn() loses that receiver in strict mode. An arrow keeps this from its enclosing scope; it does not acquire a new receiver through obj.arrow().

Objects have their own properties and a prototype chain. A missing own property can still be found on the prototype. Use Object.hasOwn when ownership matters. Prefer Map for arbitrary key/value lookup when object-prototype behavior would be surprising. These rules explain callbacks and objects; you rarely need to build a custom inheritance tree for a Vue page.''',
 '''```js
function counter() {
  let value = 0
  return () => ++value
}
const a = counter(), b = counter()
a() // 1
a() // 2
b() // 1: separate closure

const formatter = { prefix: 'Ticket', label(id) { return `${this.prefix} ${id}` } }
const detached = formatter.label
const safe = formatter.label.bind(formatter)
safe(4) // 'Ticket 4'
// detached(4) throws when this is undefined in strict mode.
```

A timer callback reading a mutable selectedId will see its later value. Pass the intended ID as a local argument if the operation should belong to the original selection.''',
 '''Trace creation → retained binding → callback invocation. Distinguish the value at registration from the value at execution. Then trace the call expression to find this.

For object lookup, check own properties first, then the prototype chain. Object.create(null) has no usual Object prototype; it also lacks methods such as hasOwnProperty. Object.hasOwn(obj,key) works without calling a method from untrusted input.''',
 'A callback can keep large objects alive after the screen closes. A detached method can lose this. Checking obj[key] alone can confuse absent values with inherited properties or valid falsey values.',
 'A detached formatter method fails when passed as a callback. Fix it two ways and explain when each is appropriate.',
 'Bind the intended receiver once or wrap the call in an arrow that explicitly calls formatter.label(id). Test the callback invocation form. Do not assume an arrow assigned as an object property receives the object as this.',
 'A delayed save uses the newly selected ticket ID instead of the ID at click time. What should be captured?',
 'Capture the intended operation input in a local value at the click boundary, and pass that value into the async operation. Still validate permissions and current version on the server. Closure mechanics do not resolve concurrent edits.',
 [q('Does a closure always freeze a variable value?','Yes','No, it keeps access to the binding','Only in strict mode',1,'The binding can still hold a later value.'),q('Where does an arrow get this?','From its enclosing scope','From every object that stores it','Always window',0,'Arrow this is lexical.'),q('How do you check an own property safely?','Object.hasOwn(obj,key)','Only obj[key]','Assume every key is own',0,'Prototype lookup and own ownership differ.')],
 'Creation decides scope. Calling decides normal this.', ['Create function','Retain binding','Call with receiver','Read current value','Release unused callback'], [('MDN closures',MDN+'JavaScript/Guide/Closures'),('MDN this',MDN+'JavaScript/Reference/Operators/this')],usecase='Event handlers, timers, reusable utilities, and callback APIs.',benefits='Makes callback behavior predictable.',drawbacks='Retained state and implicit receivers can hide ownership.',tags=['javascript','closures','objects'])

chapter('frontend','css-layout','CSS layout: size, flow, Flexbox, and Grid','beginner',
 'Choose a layout from content behavior and debug overflow instead of adding random widths.',
 '''Normal flow is the starting point: blocks stack and inline content flows within a line. The box model adds padding and border around content. box-sizing:border-box makes a declared width include padding and border. It does not make every child shrink automatically.

Use Flexbox for one-dimensional distribution: a toolbar, row, or column. Use Grid when rows and columns should align together. A flexible item may refuse to shrink below its min-content size. min-width:0 on the right child or minmax(0,1fr) on a grid track often fixes a long code/title overflow. Find the actual owner before applying it everywhere.

Responsive design follows content constraints. A breakpoint is where this layout stops working, not a universal device category. Use relative sizing, wrapping, and a readable line length. Keep DOM reading order sensible instead of using visual order to repair confusing markup.''',
 '''```css
* { box-sizing: border-box; }
.workspace {
  display: grid;
  grid-template-columns: minmax(180px, 240px) minmax(0, 1fr);
  gap: 1.5rem;
}
.results { min-width: 0; }
.toolbar { display: flex; flex-wrap: wrap; gap: .75rem; }
pre { overflow-x: auto; max-width: 100%; }
@media (max-width: 48rem) {
  .workspace { grid-template-columns: 1fr; }
}
```

The code block scrolls inside its panel. It should not make the entire page wider than the viewport. Test a long unbroken identifier, browser zoom, and translated text.''',
 '''Inspect the overflowing element's bounding box. Walk to its grid/flex parent. Check min-size, fixed width, padding, and white-space. Change one rule, observe the effect, then remove temporary patches.

A 100vw child plus body padding can overflow. A fixed-height card can cut off translated text. Avoid hiding overflow as the first repair because it can conceal controls or focused content.''',
 'A layout can look correct with short English text and fail with a long title or 200% zoom. overflow:hidden can hide the symptom while clipping important content.',
 'A two-column workspace overflows when a long code sample appears. The right column uses 1fr. Diagnose the min-size boundary and repair it.',
 'Use minmax(0,1fr) and/or min-width:0 at the actual flex/grid child. Give the code block its own horizontal scroll. Verify document scroll width at narrow widths, long strings, and zoom; do not simply clip the page.',
 'The toolbar grows from two actions to six and must work on mobile. What should determine the layout change?',
 'Try wrapping and preserve logical action order. Switch layout when labels and touch targets no longer fit comfortably. Test real labels, keyboard focus, and translated text instead of relying only on a named phone width.',
 [q('What does border-box include in declared width?','Content, padding and border','Margin too','Only text',0,'Margins remain outside the border box.'),q('Why can a 1fr track overflow?','Its automatic minimum can preserve min-content width','Grid never responds','Only a browser bug',0,'A zero minimum lets the track shrink deliberately.'),q('What should choose a breakpoint?','The point where content no longer works well','Only a device brand','Always 768px',0,'Breakpoints should serve this content and layout.')],
 'Find the box that refuses to shrink.', ['Content flow','Box and min-size','Grid or Flexbox','Constrained overflow','Narrow and zoom checks'], [('MDN CSS layout',MDN+'CSS/Guides/Layout'),('MDN grid',MDN+'CSS/CSS_grid_layout')],usecase='Support dashboards with sidebars, toolbars, and long technical content.',benefits='Responsive pages that survive real content.',drawbacks='Nested min-size and overflow rules require inspection.',tags=['css','responsive','layout'])

chapter('frontend','css-systems','CSS cascade, tokens, and component states','intermediate',
 'Explain why a style wins and build consistent states without escalating selector strength.',
 '''The cascade considers origin/importance and layers before specificity and source order. A more specific selector is not always the winner across different layers or important rules. Inspect the computed-style panel to see the actual winning declaration.

Use small component selectors and explicit state attributes/classes. Design tokens give repeated choices a name: spacing, surface, border, text, focus, and danger. A token system helps consistency; it does not justify low contrast or shrinking a label to fit.

A component has states beyond the happy screenshot: hover, focus-visible, disabled, busy, invalid, empty, and high contrast preferences. Focus must remain visible against each surface. A disabled appearance is not a substitute for explaining why an action is unavailable.''',
 '''```css
:root { --space-2: .5rem; --focus: #006c88; }
.ticket-action { padding: .65rem 1rem; border: 1px solid currentColor; }
.ticket-action:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.ticket-action[aria-busy="true"] { cursor: progress; }
@media (prefers-reduced-motion: reduce) {
  .progress-pulse { animation: none; }
}
```

Keep destructive color separate from ordinary selection. Give errors text and a field association, not only a red border.''',
 '''Select the element. Read computed style and the crossed-out rules. Locate origin/layer, selector, and source order. Remove accidental global leakage instead of adding another !important.

Then inspect every state in the same container and theme. Token changes need representative screens, long text, zoom, and focus checks. A contrast check is necessary for relevant colors; it does not test whether the task is understandable.''',
 'A global button rule can break one nested form. Repeated !important patches make the next change harder. Color-only state is invisible to some users.',
 'A component focus outline disappears under a global outline:none rule. Repair the ownership and verification plan.',
 'Remove or scope the blanket reset, define focus-visible in the component/system layer, and inspect the actual cascade. Test keyboard focus on light/dark surfaces, zoom, and dialogs. Do not restore an outline only on hover.',
 'A theme introduces new status colors. What evidence should accompany the change?',
 'Show relevant contrast measurements, text/icon labels independent of color, keyboard focus, and representative error/busy/disabled states. Preserve the meaning of danger versus selection. A token name alone is not usability evidence.',
 [q('Is specificity the first and only cascade rule?','Yes','No, origin/importance/layers also matter','Only for Vue',1,'Inspect the actual cascade rather than escalating selectors.'),q('What should an error communicate?','Text and field association as appropriate','Only red','Only an animation',0,'Meaning must not depend only on color.'),q('What is a token?','A named design choice used consistently','Automatic proof of accessibility','A CSS security role',0,'Tokens support consistency but still require evaluation.')],
 'Inspect the winner. Name the choice. Test the state.', ['Computed style','Cascade ownership','Named tokens','Component states','Keyboard and contrast checks'], [('MDN cascade',MDN+'CSS/CSS_cascade/Cascade'),('WCAG quick reference','https://www.w3.org/WAI/WCAG22/quickref/')],usecase='Shared components, themes, and regressions across screens.',benefits='Predictable styles and consistent interactions.',drawbacks='System-wide changes need representative state checks.',tags=['css','design-system','accessibility'])

chapter('frontend','dom-lifecycle','DOM events, cleanup, and resource ownership','intermediate',
 'Trace event propagation and release listeners, timers, observers, and subscriptions with their owner.',
 '''An event travels through capture, target, and bubble phases when the event supports propagation. target is where it originated; currentTarget is the element whose handler is running. Event delegation puts a handler on a stable ancestor and checks the relevant descendant. It is useful for dynamic lists, but needs a precise match and containment check.

preventDefault cancels a supported default action. stopPropagation changes event propagation. They solve different problems. A button inside a form defaults to submit unless its type says otherwise. Correct HTML often avoids a JavaScript workaround.

Every long-lived resource needs an owner: window listener, timer, ResizeObserver, WebSocket, and subscription. Vue watchers created synchronously in setup are linked to the component; manually created resources still need cleanup. A watcher created later outside that scope may need explicit disposal.''',
 '''```ts
import { onMounted, onUnmounted } from 'vue'
const onResize = () => { /* measure only what this component owns */ }
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
```

Use the same function identity when removing the listener. removeEventListener('resize',()=>work()) does not remove a different arrow registered earlier. Disconnect observers and close subscriptions through their own APIs.''',
 '''Open a screen → register resource → use it → navigate away → cleanup → reopen. Observe that only one listener/subscription remains active. Repeated mounting should not multiply calls.

For a nested icon click, compare target with currentTarget before reading dataset values. A handler attached to the button can use currentTarget for the button's data. Do not trust DOM attributes as server authorization.''',
 'Repeated route visits can accumulate listeners and duplicate saves. A Cancel button without type=button can accidentally submit a form. stopPropagation does not automatically prevent navigation or form submission.',
 'A component adds an anonymous window listener on every mount and removes a new anonymous function on unmount. Fix the leak and test remount behavior.',
 'Keep one stable handler reference per component instance, register on mount, and remove that same reference on unmount. Test mount/unmount/remount and dispatch one resize: the callback should run only for the live instance. Inspect additional timer/observer ownership too.',
 'A button contains an SVG icon. Clicking the icon gives no data-id. Why, and what should change?',
 'The target can be the SVG child. Use a handler on the button and read currentTarget, or use a precise delegated closest match plus containment check. Keep keyboard activation and correct button semantics.',
 [q('Does stopPropagation prevent form submission by itself?','Yes','No','Only in capture',1,'Propagation and default action are different.'),q('Which reference removes a listener?','The same registered function identity','Any equal-looking arrow','Only its function name text',0,'Removal matches the actual handler identity and capture option.'),q('What is currentTarget?','The element whose listener is running','Always the deepest child','The selected store record',0,'target and currentTarget answer different questions.')],
 'If you open it, own its close.', ['Mount owner','Register resource','Handle correct target','Unmount cleanup','Remount without duplicates'], [('MDN event bubbling',MDN+'API/Document_Object_Model/Event_bubbling'),('Vue lifecycle',VUE+'lifecycle.html')],usecase='Route transitions, realtime UI, resize handling, and forms.',benefits='Fewer duplicate actions and retained screens.',drawbacks='Resource ownership is separate from rendering correctness.',tags=['javascript','dom','lifecycle'])

chapter('frontend','rendering-budget','Browser rendering and performance evidence','intermediate',
 'Separate network, JavaScript, layout, paint, and rendering costs before optimizing a screen.',
 '''A slow screen can wait on a network response, execute too much JavaScript, repeatedly measure layout, paint a large area, or render too many DOM nodes. Each needs different evidence. A fast SQL query does not prove a fast interaction.

The browser builds style/layout information and paints/composites the result. Reading layout after changing styles can force work earlier than expected. Repeating write → read → write → read in a loop can create layout thrashing. Batch reads and writes when the trace shows this problem.

Measure a user task on representative data and a constrained device. Separate initial load from later interaction. Averages can hide a slow tail. Use a performance recording, network timing, bundle analysis, and Vue profiling to locate the bottleneck. Optimize that boundary, then rerun the same task.''',
 '''```js
// Avoid repeatedly interleaving style writes with layout reads.
const widths = cards.map(card => card.getBoundingClientRect().width)
cards.forEach((card, i) => { card.style.setProperty('--measured-width', `${widths[i]}px`) })
```

This is only useful when measurement is actually needed. CSS layout can often express the goal without JavaScript measurement at all. requestAnimationFrame schedules before a frame; it does not make expensive work free.''',
 '''Record open-ticket → filter → select → edit using the same fixture. Mark request start/end and visible response. Inspect long tasks, style/layout, paints, and component updates. Check the slow path after the proposed repair.

Virtualizing a list reduces DOM work but changes focus, search, row sizing, and screen-reader behavior. Memoization can add invalidation complexity. Choose the smallest fix supported by the recording.''',
 'Optimizing only the bundle can leave a long interaction unchanged. A desktop-only recording can hide low-end-device delay. A synthetic score is not the same as every real user outcome.',
 'A 5,000-row table blocks selection. The API is fast. Give a measurement and repair plan.',
 'Record the selection task with representative rows, inspect scripting/layout/component work, and first reduce unnecessary updates. Consider pagination or virtualization if DOM cost dominates. Check focus and scrolling behavior, then compare the same task before/after. Do not assume a cache fixes rendering.',
 'The first load is slow but interactions are fast. Where should you look first?',
 'Inspect network waterfall, caching/compression, image sizes, code splitting, main-thread startup, and the meaningful-content path. Use the actual trace. Preserve correctness and accessible content while deferring nonessential work.',
 [q('Does requestAnimationFrame make heavy work cheap?','Yes','No','Only in Vue',1,'Scheduling does not remove CPU cost.'),q('What can trigger repeated forced layout?','Interleaving DOM writes and layout reads','A stable string constant','Only DNS',0,'The browser may need fresh layout before returning measurements.'),q('What should follow a performance repair?','Repeat the same task and check regressions','Only a new abstraction','Only fewer lines',0,'Comparable evidence tests whether the change helped.')],
 'Measure a task. Fix the costly boundary. Measure again.', ['Representative task','Performance trace','Locate costly boundary','Small targeted repair','Compare and check access'], [('MDN critical rendering path',MDN+'Performance/Guides/Critical_rendering_path'),('Vue performance','https://vuejs.org/guide/best-practices/performance.html')],usecase='Large workspaces, slow devices, and measurable frontend improvements.',benefits='Optimization effort follows observed user delay.',drawbacks='Lab recordings must be paired with representative conditions and regressions.',tags=['performance','browser','css'])

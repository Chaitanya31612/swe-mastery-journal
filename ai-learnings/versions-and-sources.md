# Versions, sources, and your earlier journal

Research reviewed 2026-10-27. Ideas in this course are original explanations with synthetic examples. Linked primary material supports the concepts; it is not copied as a substitute for the source. Provider fields and package versions need rechecking when you upgrade. Chapter references point to the relevant primary source.

## What is durable and what changes

The durable parts are task boundaries, permissions, evidence, validation, bounded execution, failure handling, evaluation and user control. Model names, context windows, pricing, hosted feature availability, SDK methods, and protocol versions change. No chapter requires a currently fashionable model. Compare candidates on your own fixed tasks.

The runnable lab pins Ruby 3.3.6, Rails 7.2.2.2, MCP Ruby SDK 1.8.2, OpenAI Ruby SDK 0.113.0, and pgvector 0.8.1 on PostgreSQL 16. The lockfile records resolved gems. These are tested course versions, not a claim that every dependency is the newest. The MCP walkthrough selects protocol 2025-11-25; the installed SDK supports additional versions. Do not infer protocol compatibility from a gem version alone.

The optional OpenAI adapter uses the Responses API and strict JSON Schema. It is not called by the default application or its offline tests. `store: false` requests response storage behavior; it does not by itself establish a provider-wide zero-retention or no-training agreement. Check your provider terms, endpoint behavior and organizational controls. No provider API key belongs in frontend code.

Older applications may use Ruby 2.7, Rails 4.2, older Sidekiq and Vue 2. Do not paste modern gem versions or Rails APIs into such an app. Put the model boundary behind a small service or isolated gateway; keep the legacy app’s identity, policy checks and reviewed rules authoritative. Test HTTP contracts and data minimization. Plan upgrades as separate work. These labs never alter a work project.

## Your ai-mastery-journal as a bridge

Reference revision: `33d2d837d9d34713c752b5cbd1ab412e173590b8`. The journal remains unchanged. This course adds an application-engineering path rather than requiring a reread of all ML notes.

- [High-level LLM overview](https://github.com/Chaitanya31612/ai-mastery-journal/blob/33d2d837d9d34713c752b5cbd1ab412e173590b8/llm-working/HighLevelGeneralOverview.md) → stages 1–2. Use the overview as a bridge, then practise tokens, finite context, uncertainty, schemas and tool execution. “Next word” is a simplification; the model predicts tokens.
- [RAG pipeline notes](https://github.com/Chaitanya31612/ai-mastery-journal/tree/33d2d837d9d34713c752b5cbd1ab412e173590b8/rag-pipeline) → stage 3. Extend retrieval mechanics with source versions, permissions, ingestion failures, hybrid ranking, supported claims, abstention and separate retrieval evaluation.
- [PageIndex notes](https://github.com/Chaitanya31612/ai-mastery-journal/blob/33d2d837d9d34713c752b5cbd1ab412e173590b8/rag-pipeline/docs/07-vectorless-rag-pageindex.md) → advanced retrieval. Treat claimed benefits as hypotheses. Tree navigation is also an index with maintenance and query costs. Vector retrieval can preserve metadata, follow references, and use conversation history when the system is designed to do so. Compare quality, latency, price and failure cases on the same corpus.
- ML and DL notes → optional depth for model choice, tuning and serving. You can complete the developer path without reproducing training algorithms.

## Primary reference shelf

- [Transformer paper](https://arxiv.org/abs/1706.03762): attention architecture, not a guarantee about all current models.
- [RAG paper](https://arxiv.org/abs/2005.11401): retrieve external knowledge alongside generation.
- [ReAct](https://arxiv.org/abs/2210.03629): model-directed reasoning/action patterns. The course asks for observable decisions and tool results, not hidden chain-of-thought.
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), and [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices): API contracts and evaluation practices. Read current docs before changing an adapter.
- [Anthropic’s effective agent patterns](https://www.anthropic.com/research/building-effective-agents): workflows, agents and added complexity.
- [MCP 2025-11-25 specification](https://modelcontextprotocol.io/specification/2025-11-25), [authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization), and [Ruby SDK](https://github.com/modelcontextprotocol/ruby-sdk): roles, lifecycle, transport and implementation. Local training identity is not production OAuth.
- [pgvector](https://github.com/pgvector/pgvector): distance operators, exact versus approximate search, filtering and index tradeoffs.
- [Rails 7.2 Active Job](https://guides.rubyonrails.org/v7.2/active_job_basics.html): execution adapters and jobs. The local async adapter is not durable infrastructure.
- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html): layered controls. Prompt wording alone does not enforce authorization.
- [GraphRAG](https://arxiv.org/abs/2404.16130), [PageIndex implementation](https://github.com/VectifyAI/PageIndex), [LoRA](https://arxiv.org/abs/2106.09685), and [PagedAttention](https://arxiv.org/abs/2309.06180): optional deeper routes for a measured need.

JEV is intentionally omitted. The course focuses on reusable application engineering decisions rather than covering every new product.

## Evidence labels

**Illustrative fragment:** explains a mechanism; may require surrounding setup. **Offline runnable lab:** real Rails, PostgreSQL/pgvector and MCP SDK, with scripted model responses. **Provider adapter contract check:** a fake SDK client checks request/response handling; it is not a paid model experiment. **Live model evaluation:** you supply approved synthetic cases and run a selected provider separately. Keep those labels in your own reports.

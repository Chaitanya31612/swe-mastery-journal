# Transfer assessment and graduation evidence

Learning outcome: Demonstrate unaided reasoning on three different problem families and review a real architecture from evidence.

## Graduation asks for transfer, not a diagram collection

You have practiced mechanisms for lookup, concurrent claims, identity, placement, async processing, derived views, live delivery, indexing, and large-object synchronization. The final question is whether you can select and combine them when the product name changes. Do not open the solutions before submitting attempts.

Use Contract → Size → Model → Flow → Stress → Operate → Explain from memory. Narrow the scope, make assumptions visible, choose one authoritative state boundary, trace a real flow, and deep-dive the dominant risk. Spend 45 minutes per round plus 15 minutes evidence-based feedback. For three rounds this is three hours; use the remaining hour to finalize/review the real-system artifact started in module 15.

## What the examiner should change

For a read-heavy system, change freshness/access or skew. For an async pipeline, introduce a lost acknowledgment or a constrained dependency. For a correctness system, introduce a competing writer or failed ownership transfer. The purpose is to expose the mechanism, not to add every possible feature. If you already practiced a listed prompt, ask a coach for a structurally different product while preserving the family and assessment scope.

## Scoring and confidence

Use the eight dimensions in the assessment rubric, with an example of your reasoning for each score. A passing full round needs 18/24, every dimension at least 2, an intact central invariant, and unaided adaptation. This threshold is a course policy. Self/AI evaluation can miss errors; have an experienced peer challenge at least one guarantee where possible.

Ask for a minimal counterexample: two actors, one crash, one partition, one old version. If the mechanism breaks, repair it explicitly rather than defending a label. Preserve first attempts and disclose hints. MCQ success or identical diagram shapes cannot substitute for these artifacts.

## After graduation

Maintain one short mixed mock, feedback, and due retrieval each week. At work, review a new change using the same structure: user contract, data/atomicity, flows, failure, observation, and evolution. Before Volume 2, select specific gaps, not a generalized belief that everything has been forgotten. A forgotten codec name or vendor setting can be looked up; recovering the core reasoning is the retention goal.

## Retrieve before practicing

After two weeks, organize a new problem from memory, identify the central invariant, and justify the two highest-priority deep dives.

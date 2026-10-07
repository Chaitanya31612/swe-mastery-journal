# Learning protocol

## Why the activities are structured this way

Practice testing and distributed practice have broad support in learning research. The course therefore asks you to retrieve mechanisms without notes and revisit them after delays. A good-looking notebook is an artifact of study, not proof of retrieval. [Dunlosky et al.](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html).

Worked examples, self-explanation, and fading steps are useful when moving from studying solutions to independent problem solving. We use a fully annotated example, then fewer prompts, then a blank-page problem. Guidance should decrease as skill grows. [Atkinson, Renkl, and Merrill](https://eric.ed.gov/?id=EJ678596).

Retrieval can improve meaningful learning as well as factual recall; that motivates explanation and inference questions, not only flashcards. The underlying experiments do not establish that this particular HLD course is optimal or guarantee interview performance. [Karpicke and Blunt](https://pubmed.ncbi.nlm.nih.gov/21252317/).

## Before, during, and after an attempt

Before opening a solution, write your prediction: the dominant risk, the invariant, and the likely architectural decision. During the attempt, say the reason for each component aloud. After feedback, identify a counterexample your original design mishandled. Repair that mechanism and later solve a changed problem without opening the repaired answer.

For a worked example, cover the next paragraph and predict the next decision. Ask: why does this step follow from the requirement? What would make it unnecessary? Copying the diagram does not count. In a partially guided exercise, fill missing reasoning before looking at the answer. In a final exercise, do not use the framework sheet until the timer ends.

## Recall queue

Schedule approximately +1, +3, +7, +14, +30, and +60 days from an attempt. These are convenient defaults, not uniquely optimal intervals. Keep the weekly review budget to one hour: six short retrieval blocks, or three 20-minute blocks. Review failures and high-impact decisions first. Later reviews can substitute for new material when gaps accumulate.

- +1: explain the main flow in five minutes.
- +3: answer one failure question in five minutes.
- +7: redraw in ten minutes, including durable acknowledgment.
- +14: compare with a different system in ten minutes.
- +30: solve a changed-constraint mini-design in ten minutes.
- +60: use the mechanism in a mixed mock.

Mark each as **retrieved**, **partly retrieved**, or **needed reference**, with the actual missing mechanism. When you fail, attempt first, inspect only the gap, then retry tomorrow. When recall is easy, extend the gap or make the scenario less familiar. Mix older problem families only after you have initially learned their mechanisms.

## Decision cards

Keep about 20–30 high-value cards, not a transcript of the course. Each card asks a decision question and records constraint → choice → alternative → cost → failure → condition that changes the choice. Examples: “A sender timed out after the message might have persisted: how do we avoid duplicates?” and “A celebrity dominates one key: why does adding shards not automatically fix it?”

Use confidence predictions before attempts, then compare with observed performance. Feeling familiar while reading is not the same as producing the reasoning without help. A correct multiple-choice selection with no explanation or elimination of alternatives is provisional.

## If you get stuck or fall behind

Use the smallest counterexample: two concurrent requests, one crashed worker, one unavailable replica, one hot key. Trace state before/after each step. Ask for one narrow hint and label the attempt assisted. Repair the mechanism, then reattempt after a delay.

Keep three active gaps. Reduce new reading before removing retrieval. Never restart the whole book because one mechanism is rusty. If your schedule changes, record the change and move the checkpoint honestly; do not convert “read” into “mastered.”

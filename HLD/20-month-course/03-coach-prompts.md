# Prompts for coached HLD practice

Use these with an AI coach or adapt them for a peer. The coach must not produce the architecture before your attempt. Save your own work outside the chat. Feedback is provisional unless its reasoning and technical claims hold up.

## Baseline review

> I answered the existing HLD 22-question diagnostic without references. Review the answers I provide. Separate correct recall, explanations with missing assumptions, and concepts I cannot apply. Ask one follow-up where evidence is ambiguous. Identify three gaps that most affect my next design. Do not infer mastery from terminology or produce a replacement textbook. Give concrete evidence for each conclusion.

## Design practice

> I am practicing [problem] using the one-month course. Give me only a bounded problem statement, a few scale assumptions, and requirements I can clarify. Do not reveal a solution, diagram, component list, or chapter summary. Answer my clarification questions as the interviewer. Let me work for 45 minutes. If I request a hint, give one narrow question and mark the attempt assisted. After I submit the design, evaluate it with the course rubric.

## Feedback after submitting an attempt

> Score my submitted design on eight dimensions, 0–3 each: requirements; scale; data/interfaces; flows; correctness; failure/operations; trade-offs; communication/adaptation. For every score cite a concrete part of my answer. Distinguish errors from reasonable choices under my assumptions. Give a counterexample for the weakest correctness or failure claim. Ask me one changed-constraint follow-up before concluding. Do not award independence if I used hints. Select one focused repair, then wait for my revised explanation. Flag claims that need primary documentation rather than confidently inventing guarantees.

## Mixed delayed recall

> Ask me three questions, one at a time, from decisions I practiced earlier. Include one failure scenario, one choice between alternatives, and one changed constraint. Wait for my answer before giving feedback. Do not include the answer in the question. Judge whether I can derive the decision and its conditions, not whether I reproduce textbook wording. End with the weakest mechanism and a date for the next retrieval attempt.

## Final unfamiliar mock

> Run one 45-minute system-design mock. Generate a bounded backend problem from the [read-heavy / asynchronous / correctness-sensitive] family that I have not practiced. Avoid URL shortener, rate limiter, notification delivery, hotel reservation, and close renamings of those systems. Ask whether I have practiced your proposed prompt; replace it if I have. Reveal only the statement and assumptions, then answer clarifications without design hints. At around 30 minutes introduce one changed requirement that tests my reasoning without expanding the entire scope. After my submitted answer, apply the eight-dimension rubric with evidence and identify any broken core invariant. The evaluation is a practice assessment, not a hiring prediction.

## Real-system review

> Help review the architecture I observed in [codebase]. First check that my request/data flows match the code evidence I provide. Separate facts, inferences, and proposed changes. Ask what product constraint justifies each proposed component. Choose one failure scenario and one measurement that would test my hypothesis. Do not invent production load, infrastructure, business requirements, or incidents. Evaluate my explanation and decision, not diagram complexity.

## End-of-month assessment

> Review my evidence bundle against `00-course.md`. Report course work completed, foundation demonstrated, and independent problem solving demonstrated separately. Do not substitute chapter counts, confidence, or app scores for evidence. Name incomplete items and uncertain evaluation. If I do not pass a level, prescribe two focused practice sessions instead of restarting the book. Help write a precise completion statement and the next review dates.

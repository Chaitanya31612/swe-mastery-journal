# HLD attempt template

Copy this file for each attempt, using a name such as `url-shortener-attempt-1.md`. Keep the first attempt intact; write repairs and later attempts separately. This template is blank by design: fill it with your own reasoning.

## Attempt record

- Problem:
- Date and time:
- Time limit / actual time:
- Mode: unaided / assisted / open-book repair
- Previously encountered this problem?
- References or hints used and when:

## Requirements and assumptions

- User and core use case:
- Two or three required features:
- Out of scope:
- Most important NFR and how it is measured:
- Core correctness invariant:
- Assumptions I would clarify with the interviewer:

## Estimates that affect choices

- Users, operations/user, read/write mix:
- Average and peak operation rates, labeled by layer:
- Storage/object sizes/retention, units, replication/index assumptions:
- What these estimates change:
- Most uncertain assumption:

## Interfaces and data

- Important API contract(s):
- Source of truth and access patterns:
- Entities, keys, indexes, or partition key:
- Transaction/atomicity boundary:
- Consistency/freshness requirement:

## Architecture and flows

Draw here, or attach a diagram. Include one successful write and read/background flow. Label ownership and durable acknowledgment points.

- Write flow:
- Read/background flow:
- Most likely bottleneck and the metric that would confirm it:
- The main deep dive:

## Failure, operation, security, and cost

- Dependency timeout or partial failure:
- Retry/duplicate/ordering behavior and guarantee boundary:
- Recovery or degraded behavior:
- Useful user-facing SLI/SLO and alert:
- Authorization/data sensitivity:
- Main cost driver:
- Backup/restore or RPO/RTO where relevant:

## Decisions and changed constraint

- Choice, constraint, alternative, accepted downside:
- What changes at 10× load or under a new requirement:
- What needs measurement/verification before implementation:

## Feedback and repair

- Three consequential differences from review/book:
- Concrete counterexample to the weakest part of this attempt:
- Corrected mechanism and its assumptions:
- Next unaided exercise:

## Rubric evidence

Score each 0–3 and attach one concrete sentence/flow as evidence. Criteria are in `00-course.md`.

- Requirements: score / evidence
- Scale: score / evidence
- Data and interfaces: score / evidence
- Flows: score / evidence
- Correctness: score / evidence
- Failure and operations: score / evidence
- Trade-offs: score / evidence
- Communication and adaptation: score / evidence
- Total out of 24:
- Any critical broken invariant?
- Reviewer and uncertainty in evaluation:

## One decision card

- Question I must be able to answer later:
- Constraint:
- Choice:
- Credible alternative:
- Downside:
- Failure response:
- Condition that changes my choice:
- Source checked, if needed:
- Later recall dates/results: +1, +3, +7, +14, +30, +60 days

# Evaluation workbook · an average can hide a serious failure

This is a teaching dataset with saved, hand-written decisions. No model was run to produce them. Some scenarios describe a future extension of the lab, such as clarification or a policy answer. Do not report them as all implemented Rails endpoints.

Run this from the Dispatch Desk training folder using Python 3:

```bash
python3 evaluation/score_predictions.py evaluation/teaching_predictions.jsonl
```

Expected: 10 correct out of 12. The average looks promising, but the foreign-record decision fails. The release gate says **hold**. It also lists the ambiguous-depot mistake. Repair the system, not just the saved answer file.

Read cases.jsonl. Each row defines an input, expected state, critical flag and a short human rubric. Those flags are exercise choices, not a universal risk model. Add realistic frequency and consequence information when evaluating a real task.

The scorer checks exact decision labels and complete case coverage. Duplicate, unknown or missing IDs are rejected so a report cannot quietly omit difficult cases. A passing decision label does not prove the output contained no leaked data or supported every sentence. Add captured-context assertions and human content review for those claims.

Next, replace the saved predictions with outputs from your own approved synthetic evaluation run. Record model, prompt, schema, retrieval version and timestamp separately. Keep development examples apart from a held-out set. Do not tune on the held-out answers after every small change.

Practice: add three original cases, including a valid alternative and an uncertain outcome. Explain which checks are deterministic, which need human review, and why a model judge may disagree. Never treat a judge score as evidence that an unrun command passed.

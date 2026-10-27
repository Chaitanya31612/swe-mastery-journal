# Tell the model one clear job

A prompt is a set of instructions for a model call.

Say what to do, what evidence to use, and what the answer should look like.

## A small example

> **Task**
>
> Turn this sentence into an allowed shipment filter.
>
> If the depot name matches two places, ask which one. Do not guess.

```text
Task + allowed evidence + output shape + what to do when unsure
                              ↓
                         Model proposal
                              ↓
                    Code validates the result
```

“Be accurate” is too vague to be a useful rule by itself.

## Show more than the happy path

Give a normal example, an unclear example, and an unknown example.

These are **few-shot examples**: a few demonstrations of the behavior you want.

Do not let an example quietly grant extra permissions or invent a default value.

## Keep instructions separate from outside text

User messages, documents, and tool results can contain hostile instructions.

Roles and delimiters help show the boundary. They do not enforce access rules.

Keep the prompt and its output checks under version control together.

## Remember

Give the model clear instructions. Let code enforce the rules.

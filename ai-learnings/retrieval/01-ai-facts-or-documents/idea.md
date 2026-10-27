# First decide where the answer lives

Some answers come from current database records. Others need documents.

Choose the source before choosing an AI tool.

## A small example

- “How many parcels are held?” → run an allowed database query.
- “What does the dispatch policy say?” → find an allowed policy document.
- “Why is this parcel held?” → check its current fields and the reviewed hold rules.

```text
Question → current facts, documents, or both → answer with its sources
```

Keep counts and exact rules in code.

## What RAG adds

**RAG** means finding relevant material and giving it to the model before it answers.

A simple version might search a document table and include the matching passages in the request.

You can use exact IDs, filters, or full-text search. Add semantic search when differences in wording make those methods miss useful material.

## What RAG does not prove

Retrieved text can be old, irrelevant, or outside the user’s access.

The model can also write a claim that the text does not support.

Keep permission checks, source versions, and answer checks visible.

## Remember

Use live data for live facts. Use documents for document knowledge. Check both before showing an answer.

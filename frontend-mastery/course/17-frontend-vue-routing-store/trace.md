## Trace the execution

Direct URL → parse query/params → establish workspace context → load allowed server data → render → user changes filter → update URL. Back navigation should restore meaningful state.

For an unsaved form, define whether navigation prompts, saves a draft, or discards it. Browser Back and an in-app link should follow the same user-facing policy.
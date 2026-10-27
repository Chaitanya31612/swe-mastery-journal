## Trace the execution

Type → dirty draft → client checks → request with expected version → server validation/authorization → success or conflict → keep or reconcile draft.

An old successful response must not overwrite newer edits typed during the request.

Test paste, keyboard submit, double-click, slow save, field rejection, network loss, and record replacement. Use a visible saving status and a clear retry path.
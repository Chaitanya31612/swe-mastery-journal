# Follow the execution

Draw the relation-building calls before the first SQL. Then draw the initial task query and the association-loading query. With a simple belongs_to preload, adding more tasks should not add one owner query per task.

Compare one task and twenty tasks. Confirm the response needs each loaded field. An association cache on already loaded objects can make a repeated access look cheap; start the measurement with fresh records.

# What can go wrong

Calling size, count, and length can have different SQL behavior depending on loaded state. A Ruby block passed to select after loading does not become a SQL WHERE clause.

**Memory cue:** Build the query. Ask for rows.

Count the SQL.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.
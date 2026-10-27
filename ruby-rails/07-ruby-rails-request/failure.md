# What can go wrong

Task.find(params[:id]) plus permit(:title) still allows an ownership bug. Strong parameters protect allowed attributes, not which task you can edit. Never permit owner_id just because the browser sent it.

**Memory cue:** Who? Which row? Which fields?

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

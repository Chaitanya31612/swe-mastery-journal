# The idea

Source state is information you choose to store. Derived state can be calculated from it.

If tasks and a filter are stored, visibleTasks can often be derived. Storing both copies creates a synchronization job you may not need.

URL state belongs in the URL when users should bookmark, refresh, or share it, such as search and page. Server state is remote data with freshness and loading concerns.

Local UI state includes an open tooltip or unsaved input. A global store is not the default home for everything.

Give each fact one clear owner. Other places read it or send updates through that owner.

A cache is another copy with a freshness policy, not a new unquestioned source of truth.
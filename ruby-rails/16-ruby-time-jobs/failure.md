## Break it and reason about the repair

A mutex in one Ruby process does not coordinate multiple schedulers. A UTC date and a user-local date can refer to different report periods.

A done flag written before the effect can lose work.

**Remember:** A time is not a date. A tick is not a completed run.
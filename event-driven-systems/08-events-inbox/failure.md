## Break it and reason about the repair

Writing inbox before the effect in a separate committed transaction can lose the effect. Writing it after can duplicate. A memory Set disappears on process restart.

**Remember:** Dedup plus local effect together. Offset after.

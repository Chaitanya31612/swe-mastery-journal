## Break it and reason about the repair

Using value || default can silently change a valid zero. Copying only the outer object can leak draft changes.

Parsing valid JSON can still produce the wrong type.

**Remember:** Absence is a contract. Copy only what you own.
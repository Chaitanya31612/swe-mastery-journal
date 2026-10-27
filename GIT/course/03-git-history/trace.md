# Follow the execution

Draw O→A on main and O→B→C on your branch. Merge can produce a node with A and C as parents.

Rebase builds B′ and C′ on A. The old B/C objects may still exist, but your branch now names C′.

For each conflict, read the common base, both edits, and nearby call sites. Test the combined result.

Record a short explanation when the merge resolution makes a meaningful product decision.
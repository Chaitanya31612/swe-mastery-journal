# Follow the execution

After add, the index holds A. After editing, the working tree holds B.

A commit records A. The remaining A→B difference stays in the working tree.

Draw HEAD → commit → tree → blob, then draw the index as a separate proposed tree.

This model explains partial staging, restore, reset, and why a clean diff is not always a clean staged snapshot.
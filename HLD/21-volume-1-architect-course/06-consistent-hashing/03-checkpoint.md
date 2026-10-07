# Consistent hashing, placement, and migration — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. Adding a node changes which ring interval?
   - A. Every key necessarily
   - B. Only keys after zero
   - C. A node-independent fixed amount
   - D. The predecessor-to-new-node ownership interval

2. Three replica virtual nodes on one physical machine provide what?
   - A. Poor protection from that machine failing
   - B. Three independent failure domains
   - C. Guaranteed regional durability
   - D. A safe quorum automatically

3. A hot key is best analyzed as what?
   - A. An alphabet-size problem
   - B. Access skew at the serving/serialization boundary
   - C. A reason to always increase virtual nodes
   - D. A TLS problem

4. What does consistent hashing alone NOT supply?
   - A. A placement function
   - B. Limited remapping under assumptions
   - C. Safe live data migration and durability
   - D. Successor ownership


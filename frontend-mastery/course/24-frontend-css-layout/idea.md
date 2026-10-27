## Understand the idea

Normal flow is the starting point: blocks stack and inline content flows within a line. The box model adds padding and border around content. box-sizing:border-box makes a declared width include padding and border. It does not make every child shrink automatically.

Use Flexbox for one-dimensional distribution: a toolbar, row, or column. Use Grid when rows and columns should align together. A flexible item may refuse to shrink below its min-content size. min-width:0 on the right child or minmax(0,1fr) on a grid track often fixes a long code/title overflow. Find the actual owner before applying it everywhere.

Responsive design follows content constraints. A breakpoint is where this layout stops working, not a universal device category. Use relative sizing, wrapping, and a readable line length. Keep DOM reading order sensible instead of using visual order to repair confusing markup.

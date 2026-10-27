# One valid repair

It returns one value per input, including nil for every false branch. Use select { |t| t[:done] } to filter, then map if you need IDs.

Test the result contents and size with both done and open tasks.

**How to check:** select filters original items. map transforms every item into a block result.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
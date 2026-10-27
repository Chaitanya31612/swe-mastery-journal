# Follow the execution

For map, write the block result below each input. For select, write keep/drop below each input. For reduce, write the accumulator after each step.

yield calls the provided block. A method that may be called without one can check block_given?. An Enumerator can defer iteration. lazy can avoid creating intermediate arrays, but the work still happens when a terminal operation asks for results.

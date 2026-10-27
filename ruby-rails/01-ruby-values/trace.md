# Follow the execution

Draw two arrows to the same array before the append. After second is reassigned, draw its arrow to a new array. The first arrow did not move.

Hash.new([]) uses one shared default object and does not insert missing keys when you read them. The block form above creates and stores a separate array for each new key. dup copies only one level; nested arrays can still be shared.

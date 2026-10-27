# The idea

A block is a chunk of behavior passed to a method. Enumerable gives collections common operations. Choose by the result you need: each for an action, map for one output per input, select for a subset, find for one match, and reduce for an accumulated result.

Do not memorize these as interchangeable loops. Ask what shape should come back. map preserves the number of items, even if your block returns nil. select keeps original items whose block result is truthy. each normally returns the receiver, not the block results.

Enumerable over an array runs Ruby code now. An ActiveRecord relation can build SQL lazily. relation.select(:id) and array.select { ... } do different work. Check the receiver before guessing from a method name.

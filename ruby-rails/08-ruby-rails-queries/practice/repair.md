# Find and fix the bug

A list uses Task.all.to_a.select { |t| !t.done }.first(20), then reads every owner. Repair both the row loading and association problem.

Write: prediction → proposed change → observed evidence → explanation. Run code only in a separate training sandbox. If you did not run it, say so. Submit before opening a reference.

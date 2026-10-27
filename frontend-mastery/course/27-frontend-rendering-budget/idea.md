## Understand the idea

A slow screen can wait on a network response, execute too much JavaScript, repeatedly measure layout, paint a large area, or render too many DOM nodes. Each needs different evidence.

A fast SQL query does not prove a fast interaction.

The browser builds style/layout information and paints/composites the result. Reading layout after changing styles can force work earlier than expected.

Repeating write → read → write → read in a loop can create layout thrashing. Batch reads and writes when the trace shows this problem.

Measure a user task on representative data and a constrained device. Separate initial load from later interaction.

Averages can hide a slow tail. Use a performance recording, network timing, bundle analysis, and Vue profiling to locate the bottleneck.

Optimize that boundary, then rerun the same task.
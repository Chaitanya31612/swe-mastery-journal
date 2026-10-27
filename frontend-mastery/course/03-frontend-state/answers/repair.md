# One valid repair

Keep tasks and filter as source state and derive visibleTasks during render/computed evaluation. Store only values that carry independent information.

Test changing both the filter and a task without a manual synchronization effect.

**How to check:** If it can be calculated reliably from existing state, storing another copy can create avoidable drift.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
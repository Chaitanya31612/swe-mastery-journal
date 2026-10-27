## One valid repair

Keep one stable handler reference per component instance, register on mount, and remove that same reference on unmount.

Test mount/unmount/remount and dispatch one resize: the callback should run only for the live instance. Inspect additional timer/observer ownership too.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff.

A product name or a longer answer is not proof.
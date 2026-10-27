# What can go wrong

A callback with return inside Proc.new may exit its defining method rather than only finishing the callback. Rescue does not make confusing control flow easier to maintain.

**Memory cue:** Three envelopes: values, names, behavior.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.
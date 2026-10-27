# What can go wrong

A concern can quietly add callbacks and class methods. Naming a module does not isolate its side effects. A singleton method defined on one object does not automatically become an instance method for every object.

**Memory cue:** Follow the receiver, then the lookup path.

Close this lesson. Draw the five steps. Explain one failure in your own words before opening Practice.

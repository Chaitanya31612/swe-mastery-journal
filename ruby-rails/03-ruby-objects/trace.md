# Follow the execution

For prepend, begin at the wrapper module. Its super calls the next matching implementation, Task#label.

With include, the class method normally wins before the included module.

To debug a surprising method, inspect obj.method(:name).owner and .source_location. Inspect Class.ancestors for included/prepended modules.

This turns “Ruby magic” into a path you can follow.
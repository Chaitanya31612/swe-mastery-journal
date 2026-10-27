## Understand the idea

A function can keep access to variables from the scope where it was created. That is a closure.

It captures a binding, not always a frozen copy of the value. A later mutation can change what a callback reads.

Each function call can also create a separate binding, which is why a factory can give each widget private state.

For a normal function, this depends on how it is called. obj.method() supplies obj. Taking const fn=obj.method and calling fn() loses that receiver in strict mode.

An arrow keeps this from its enclosing scope; it does not acquire a new receiver through obj.arrow().

Objects have their own properties and a prototype chain. A missing own property can still be found on the prototype.

Use Object.hasOwn when ownership matters. Prefer Map for arbitrary key/value lookup when object-prototype behavior would be surprising.

These rules explain callbacks and objects; you rarely need to build a custom inheritance tree for a Vue page.
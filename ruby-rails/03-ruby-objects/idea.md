# The idea

Every ordinary Ruby method call has a receiver. self is the current receiver. An instance method lives on a class or module; each instance supplies its own instance variables.

A class is also an object, so def self.build defines a singleton method on that class object.

include adds a module to instance-method lookup. extend adds module methods to one object’s singleton lookup. prepend puts a module before the class, so a wrapper can call super to continue the chain.

Order matters.

Class variables written @@name can be shared across an inheritance tree in surprising ways.

A class instance variable written @name on the class object is different from an instance variable on an instance. Avoid shared mutable class state when the value belongs to one request.
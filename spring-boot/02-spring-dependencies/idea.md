# The idea

Dependency injection means receiving the objects you need instead of finding or creating them inside a method. A constructor makes those needs visible. It also lets a test pass a fake.

The default bean scope is singleton: one instance per application context for that bean definition. It is not one instance for the whole internet. Several request threads can call the same service. A mutable field such as currentUser can leak data between requests. Keep request data in method arguments and local variables.

An interface is useful when it expresses a real boundary, such as sending messages. You do not need an interface for every small class. If two beans satisfy one constructor parameter, choose deliberately with a qualifier or a primary bean. Circular constructors usually signal mixed responsibilities.

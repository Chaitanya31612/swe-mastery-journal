# Follow the execution

The container sees TaskService needs a Notifier. It creates or finds ConsoleNotifier, then supplies it to the constructor.

MVC can now call the same TaskService for many requests.

For a unit test, Java calls the constructor directly with a fake. No server or application context is needed.

A context test answers a different question: did scanning, profiles, and bean selection wire the real graph correctly?
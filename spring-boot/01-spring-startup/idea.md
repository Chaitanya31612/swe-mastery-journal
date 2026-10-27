# Start with this

You write Java classes. Spring creates and connects some of their objects for you.

A Spring-managed object is called a **bean**. Spring Boot adds useful defaults so you need less setup.

## A small picture

```text
main() starts Spring
       ↓
Spring finds your components
       ↓
Spring creates beans and connects them
       ↓
The web server starts accepting requests
```

## Try this example

You add a controller for `GET /tasks`. Spring must find that controller before it can handle the request.

Keep the main application class above your feature packages. That gives component scanning a useful place to start.

Creating an object with `new` does not automatically make it a Spring bean.

## What Boot adds

Boot checks the classes and settings available to the app. It can then set up common parts, such as a web server.

This is **auto-configuration**. Your own bean can replace a default when the auto-configuration conditions allow it.

## Remember

A successful startup means the app started. Send a real request to check that the route and its dependencies work.

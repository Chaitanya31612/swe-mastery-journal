# Follow the execution

A servlet filter can run before MVC. DispatcherServlet chooses a handler. A message converter reads JSON. Validation runs on the bound input. Then the controller invokes the service. The response converter writes JSON.

Try an empty title, malformed JSON, a valid request, and a simulated service conflict. For each, predict whether the service should run. Use @RestControllerAdvice with @ExceptionHandler for your domain errors. Log a request ID so an operator can find details privately.

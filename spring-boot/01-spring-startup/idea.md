# The idea

Spring Boot builds on Spring. Spring manages objects called beans. Boot supplies useful defaults when the required classes and settings are present. This is auto-configuration. It can step aside when you define your own bean.

Your main method starts an application context. The context finds component classes, creates beans, and connects dependencies. A web application also starts an embedded server. A Java object created with new is still an ordinary object; Spring does not manage it automatically.

Start small: one application class, one controller, one request. Keep the main class above your feature packages so component scanning can find them. A green startup log only says startup succeeded. It does not prove every request or database query works.

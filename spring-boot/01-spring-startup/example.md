# A small example

```java
package learning.tasks;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
public class TasksApplication {
  public static void main(String[] args) {
    SpringApplication.run(TasksApplication.class, args);
  }
}
// Put this class in its own file, under learning.tasks.
@RestController
class PingController {
  @GetMapping("/ping")
  String ping() { return "pong"; }
}
```

```properties
# application.properties: change just this setting to try another port.
server.port=8081
```
Run the supplied Spring sandbox with Maven. Request GET /ping.

Read the startup log and find the actual port. Change the port with --server.port=8082 and predict which value wins.
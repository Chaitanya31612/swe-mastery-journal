package learning.tasks;

import java.net.URI;
import java.security.Principal;
import java.util.List;
import jakarta.persistence.*;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import static org.springframework.http.HttpStatus.*;

@SpringBootApplication
public class TasksApplication {
    public static void main(String[] args) { SpringApplication.run(TasksApplication.class, args); }

    @Bean SecurityFilterChain security(HttpSecurity http) throws Exception {
        // CSRF stays enabled. Tests show why unsafe requests need a CSRF token.
        return http.authorizeHttpRequests(r -> r.requestMatchers("/ping", "/actuator/health").permitAll()
            .anyRequest().authenticated()).httpBasic(Customizer.withDefaults()).build();
    }
    @Bean UserDetailsService users() {
        // Synthetic local training credentials. Do not reuse them in another app.
        return new InMemoryUserDetailsManager(
            User.withUsername("alice").password("{noop}training-only").roles("USER").build(),
            User.withUsername("bob").password("{noop}training-only").roles("USER").build());
    }
}

@Entity
@Table(name = "training_tasks")
class Task {
    @Id @GeneratedValue Long id;
    @Version Long version;
    @Column(nullable = false) String owner;
    @Column(nullable = false) String title;
    boolean done;
    protected Task() {}
    Task(String owner, String title) { this.owner = owner; this.title = title; }
}

@Entity
@Table(name = "training_outbox", uniqueConstraints = @UniqueConstraint(columnNames = "event_key"))
class Outbox {
    @Id @GeneratedValue Long id;
    @Column(name = "event_key", nullable = false) String eventKey;
    protected Outbox() {}
    Outbox(String key) { eventKey = key; }
}
interface Tasks extends JpaRepository<Task, Long> { List<Task> findByOwnerOrderById(String owner); }
interface Events extends JpaRepository<Outbox, Long> {}
record CreateTask(@NotBlank String title) {}
record TaskView(Long id, String title, boolean done) {
    static TaskView from(Task task) { return new TaskView(task.id, task.title, task.done); }
}

@Service
class TaskUseCases {
    private final Tasks tasks;
    private final Events events;
    TaskUseCases(Tasks tasks, Events events) { this.tasks = tasks; this.events = events; }
    @Transactional
    public TaskView create(String owner, String title) {
        if (title == null || title.isBlank()) throw new IllegalArgumentException("title required");
        return TaskView.from(tasks.save(new Task(owner, title)));
    }
    @Transactional(readOnly = true)
    public List<TaskView> list(String owner) {
        return tasks.findByOwnerOrderById(owner).stream().map(TaskView::from).toList();
    }
    @Transactional(readOnly = true)
    public TaskView read(String owner, long id) { return TaskView.from(allowed(owner, id)); }
    @Transactional
    public TaskView complete(String owner, long id) {
        Task task = allowed(owner, id);
        if (!task.done) {
            task.done = true;
            events.save(new Outbox("complete:" + id));
        }
        return TaskView.from(task);
    }
    private Task allowed(String owner, long id) {
        Task task = tasks.findById(id).orElseThrow(() -> new ResponseStatusException(NOT_FOUND));
        if (!task.owner.equals(owner)) throw new AccessDeniedException("Not your task");
        return task;
    }
}

@RestController
class TaskController {
    private final TaskUseCases service;
    TaskController(TaskUseCases service) { this.service = service; }
    @GetMapping("/ping") String ping() { return "pong"; }
    @GetMapping("/tasks") List<TaskView> list(Principal user) { return service.list(user.getName()); }
    @GetMapping("/tasks/{id}") TaskView read(Principal user, @PathVariable long id) { return service.read(user.getName(), id); }
    @PostMapping("/tasks") ResponseEntity<TaskView> create(Principal user, @Valid @RequestBody CreateTask input) {
        TaskView created = service.create(user.getName(), input.title());
        return ResponseEntity.created(URI.create("/tasks/" + created.id())).body(created);
    }
    @PostMapping("/tasks/{id}/complete") TaskView complete(Principal user, @PathVariable long id) {
        return service.complete(user.getName(), id);
    }
}

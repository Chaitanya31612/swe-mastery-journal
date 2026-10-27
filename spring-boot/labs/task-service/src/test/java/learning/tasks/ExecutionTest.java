package learning.tasks;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.transaction.PlatformTransactionManager;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class ExecutionTest {
    @Autowired MockMvc http;
    @Autowired TaskUseCases service;
    @Autowired Tasks tasks;
    @Autowired Events events;
    @Autowired PlatformTransactionManager transactions;
    @BeforeEach void clear() { events.deleteAll(); tasks.deleteAll(); }

    @Test void public_ping_and_private_list() throws Exception {
        http.perform(get("/ping")).andExpect(status().isOk()).andExpect(content().string("pong"));
        http.perform(get("/tasks")).andExpect(status().isUnauthorized());
    }
    @Test void binding_validation_and_csrf_happen_before_creation() throws Exception {
        http.perform(post("/tasks").with(user("alice")).contentType("application/json").content("{\"title\":\"hello\"}"))
            .andExpect(status().isForbidden());
        http.perform(post("/tasks").with(user("alice")).with(csrf()).contentType("application/json").content("{\"title\":\"\"}"))
            .andExpect(status().isBadRequest());
        assertEquals(0, tasks.count());
    }
    @Test void valid_request_creates_a_dto() throws Exception {
        http.perform(post("/tasks").with(user("alice")).with(csrf()).contentType("application/json").content("{\"title\":\"Learn\"}"))
            .andExpect(status().isCreated()).andExpect(jsonPath("$.title").value("Learn"))
            .andExpect(jsonPath("$.owner").doesNotExist());
    }
    @Test void owner_rule_prevents_writes() throws Exception {
        TaskView task = service.create("alice", "Learn");
        http.perform(post("/tasks/" + task.id() + "/complete").with(user("bob")).with(csrf()))
            .andExpect(status().isForbidden());
        assertFalse(tasks.findById(task.id()).orElseThrow().done);
        assertEquals(0, events.count());
    }
    @Test void repeated_completion_keeps_one_local_intent() {
        TaskView task = service.create("alice", "Learn");
        service.complete("alice", task.id());
        service.complete("alice", task.id());
        assertTrue(tasks.findById(task.id()).orElseThrow().done);
        assertEquals(1, events.count());
    }
    @Test void rollback_removes_both_state_change_and_intent() {
        TaskView task = service.create("alice", "Learn");
        TransactionTemplate tx = new TransactionTemplate(transactions);
        assertThrows(IllegalStateException.class, () -> tx.execute(status -> {
            service.complete("alice", task.id());
            throw new IllegalStateException("synthetic failure");
        }));
        assertFalse(tasks.findById(task.id()).orElseThrow().done);
        assertEquals(0, events.count());
    }
}

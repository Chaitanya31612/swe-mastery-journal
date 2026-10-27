## Follow a concrete example

```java
interface ReceiptGateway {
  ReceiptResult send(String eventKey, ReceiptRequest request);
}
// Adapter responsibilities:
// configured timeouts; bounded retries; response validation;
// stable provider idempotency key if supported;
// map accepted/rejected/unknown outcomes explicitly.
```

In a fake adapter, record acceptance and then throw a timeout. This reproduces the difficult case without sending real messages.

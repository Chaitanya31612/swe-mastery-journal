## Follow a concrete example

```java
@org.springframework.boot.context.properties.ConfigurationProperties("receipts")
@org.springframework.validation.annotation.Validated
record ReceiptSettings(
  @jakarta.validation.constraints.NotNull java.net.URI endpoint,
  @jakarta.validation.constraints.Min(1) int maxAttempts) {}
// Enable with @ConfigurationPropertiesScan or @EnableConfigurationProperties.
```
```properties
receipts.endpoint=https://example.invalid/receipts
receipts.max-attempts=3
```
Use a clearly fake endpoint in a training environment. Do not send requests to it as if it were a real provider.
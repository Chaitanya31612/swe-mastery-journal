## Trace the execution

Business change commits with a receipt intent. A worker sends it with eventKey E.

The provider accepts E but the response is lost. A retry uses E again under the provider’s documented key contract, or reconciliation resolves uncertainty when such a contract is absent.

Do not retry an entire use case if that repeats unrelated writes. Put the retry around the boundary you actually intend to repeat.
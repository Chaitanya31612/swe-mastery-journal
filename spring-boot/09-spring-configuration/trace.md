## Trace the execution

Boot prepares environment properties → binds a settings object → validates it → creates dependent clients → starts serving traffic. A bad required setting should fail at a clear boundary.

In a test, supply an invalid max-attempts and verify startup rejects it. Then verify the intended profile chooses the fake integration.

A unit test constructing the settings object does not prove binding/validation wiring.
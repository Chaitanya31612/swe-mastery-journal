## Walk through an example

The agent sends a request to create a review note. The effect succeeds, but the worker dies before marking the step complete.

On resume, a new operation identity would create a duplicate. Reuse/check the stable business identity and reconcile the recorded result.

The main Rails lab is read-only and documents its local queue limits. This chapter asks you to design the durable extension rather than pretending those limits are solved.
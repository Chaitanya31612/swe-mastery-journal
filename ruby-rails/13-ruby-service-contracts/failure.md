## Break it and reason about the repair

A service that catches StandardError and returns success hides operational defects. Passing a model from a controller does not mean it belongs to the actor’s tenant.

**Remember:** A service name is not a guarantee. Write the contract.

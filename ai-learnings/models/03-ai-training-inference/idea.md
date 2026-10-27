## Understand

Training updates model parameters from data. Inference uses a trained model to produce outputs. A normal API conversation does not mean your application is updating the model’s weights during that conversation.

Pretraining learns broad statistical patterns. Instruction tuning and preference/reward-based post-training shape useful behavior. These stages do not turn the model into your current production database. Provider data-use, logging, and retention policies are separate questions; “not training” does not mean “not stored.”

There are several places to put knowledge: weights, the current request, a retrieval index, a business database, and a stored conversation. They have different update and deletion paths. Use current scoped queries for live counts. Use retrieval for relevant documents. Consider fine-tuning for a measured behavior gap, not as the first way to keep yesterday’s inventory current.

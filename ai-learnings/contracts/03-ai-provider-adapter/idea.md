## Understand

Define a small application-owned interface such as propose_filter or explain_facts. A provider adapter builds the vendor request, sets deadlines, maps response items, and returns your own result/error type. Controllers should not know whether a provider calls something input, messages, output, or toolResult.

Capabilities still differ. Do not hide missing schema, tool, streaming, or modality support behind a uniform method name. Validate the selected combination at configuration time. Keep model identifiers in environment/configuration and record the effective version used in evaluations.

The official OpenAI Ruby SDK used in this course requires modern Ruby. The isolated lab uses Ruby 3.3 and Rails 7.2. A Ruby 2.7 / Rails 4.2 application may use a supported HTTP boundary or a separate modern gateway. Do not install this lab's gems into an existing legacy application.

## Understand the idea

TypeScript checks code before it runs. It does not validate JSON at runtime.

A cast tells the compiler what you claim; it does not turn a string into a number or verify an API response.

A discriminated union uses one field to distinguish valid shapes. A loading state does not need fake rows and an error at the same time.

Narrow the union before reading a field that exists only in one variant.

Use unknown for data you have not checked. Keep interfaces small at the component boundary.

Prefer a clear union for status to several booleans that allow impossible combinations such as loading=true and finished=true.
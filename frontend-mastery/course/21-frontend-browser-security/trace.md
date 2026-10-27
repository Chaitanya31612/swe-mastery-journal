## Trace the execution

Input arrives → validate shape → decide text versus rich content → render through the right boundary → enforce server permissions for actions. Audit the payload and telemetry, not just pixels.

Test a title containing markup-looking text. It should appear as text.

Test a direct unauthorized request without using the UI. These are different checks.
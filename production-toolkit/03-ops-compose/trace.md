## Trace the execution

Compose creates network/services → database becomes healthy → schema setup completes → web/dispatch/consumer start → service DNS connects internal calls → published port serves the browser.

Inspect logs and exit status per service. Rebuilding an image does not necessarily replace every running service unless the chosen command does so. State what the command will change.

## Understand the idea

Outside text is data. Rendering it as HTML can turn it into executable behavior.

Vue’s ordinary interpolation escapes text; v-html crosses a different boundary. If rich HTML is required, use a maintained sanitizer with an explicit policy and keep it updated.

Browser storage is available to code running in the origin. It is not a secret vault.

A script injection can read accessible tokens and drafts. Cookie settings, CSRF protection, Content Security Policy, and server access checks address different risks.

Never send a field to the browser just because it is hidden visually. Client props, network payloads, source maps, logs, and analytics can all reveal information.

Select permitted data on the server and keep telemetry deliberately small.
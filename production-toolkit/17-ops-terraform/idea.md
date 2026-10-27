## Understand the idea

Terraform describes resources through providers and tracks managed identity in state. Configuration is desired structure; state maps that structure to actual remote objects. A plan compares the chosen inputs/state/provider view with reality and proposes changes.

State can contain sensitive values. Use a deliberate backend/access/locking/recovery strategy. Two uncoordinated applies can race. Manual console changes create drift that must be understood before the next plan.

Learning setup: use a dedicated training configuration, pin provider/tool versions, review variables and account/region, run formatting/validation, inspect a saved plan, and apply only when you deliberately choose the real resource/cost changes. The course does not run apply or create AWS infrastructure.

## Trace the execution

Fix on main → inspect dependencies → replay onto release branch → resolve intent → test release configuration → review. The new commit ID can differ even when the patch is similar.

For a revert, test the resulting behavior with later changes present. A reverse patch is not a reversal of every external effect or migration.
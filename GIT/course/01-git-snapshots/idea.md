# The idea

Git stores snapshots and the links between them. A commit names a tree and parent commits. A branch name points to a commit. HEAD normally names the checked-out branch; in detached mode it points at a commit directly.

Think in three places: HEAD is the last committed snapshot, the index is the proposed next snapshot, and the working tree is the files you are editing. git add copies current content into the index. Editing again does not silently update that staged content.

Commit identity depends on content and metadata, including parents. Recreating the same file change on a different parent usually creates a different commit. A branch is a movable label, not another complete directory copy.

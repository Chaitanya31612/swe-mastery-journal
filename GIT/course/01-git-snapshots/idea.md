# Start with this

Git saves snapshots of files. A commit records a snapshot and links to its parent commits.

A branch is a movable name for a commit.

## The three places

```text
Working tree         Index / staging area         HEAD
Files you edit  ───>  Next snapshot you propose ──> Last committed snapshot
                 add                         commit
```

`HEAD` normally points to your current branch. In detached mode, it points directly to a commit.

## Try this example

Edit `app.rb`, then run `git add app.rb`. Git stages the file as it looks at that moment.

Now edit it again. The second edit stays in the working tree until you stage it too.

```text
Staged version:       first edit
Working tree version: first edit + second edit
```

## Why commit IDs change

A commit ID depends on the content and metadata, including its parents.

The same file change on a different parent usually produces a different commit ID.

## Remember

Before a commit, compare the working tree, the staged snapshot, and `HEAD`.

A branch is a label. It is not a second full copy of your project directory.

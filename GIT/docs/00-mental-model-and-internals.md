# 00 - Mental Model And Internals

Git becomes simple when you stop thinking of it as "file versions" and start thinking of it as "named pointers into an immutable graph".

---

## The Core Idea

Git stores content in an object database. Most commands either:

- create immutable objects
- move names that point to objects
- copy content between the object database, index, and working tree

The important layers:

```text
working tree
  Your editable files.

index
  The proposed next commit.

object database
  Immutable blobs, trees, commits, and annotated tags.

refs
  Human names like main, feature/login, origin/main.

HEAD
  Your current position. Usually points to a branch, which points to a commit.

reflog
  Local history of where refs used to point.
```

Once you know which layer changed, you know what happened.

---

## The Object Store

Git stores four main object types.

```text
blob
  File content. No filename. No path. Just bytes.

tree
  Directory listing. Maps names to blobs or other trees.

commit
  Points to one tree, zero or more parents, author metadata, committer metadata,
  and a message.

tag
  Usually a named annotation pointing at another object.
```

A commit does not store "the diff". A commit stores a snapshot root tree.

Diffs are computed later by comparing trees.

---

## Content Addressing

Every Git object is named by a hash of its type, size, and content.

That means:

- identical file content creates the same blob object
- changing one byte creates a different object id
- objects are immutable because changing the content changes the name
- history integrity comes from commit objects pointing to parent commit ids

Try this in a scratch repo:

```bash
mkdir /tmp/git-internals-lab
cd /tmp/git-internals-lab
git init

printf 'hello\n' > note.txt
git hash-object note.txt
git hash-object -w note.txt
```

`git hash-object note.txt` computes the blob id.

`git hash-object -w note.txt` computes and writes it into `.git/objects`.

Now inspect it:

```bash
git cat-file -t <blob-id>
git cat-file -p <blob-id>
```

Expected:

```text
blob
hello
```

Senior intuition: Git does not care that this came from `note.txt`. The blob only knows content.

---

## Trees Add Names

Blobs are anonymous content. Trees give that content names and paths.

```bash
git add note.txt
git write-tree
git cat-file -p <tree-id>
```

You will see something like:

```text
100644 blob <blob-id>    note.txt
```

The tree says:

- mode: regular file
- type: blob
- object id: the file content
- name: `note.txt`

Senior intuition: renames are not stored as special rename objects. Git infers renames by comparing similar blobs across trees.

---

## Commits Add Time And Parentage

A commit points to a tree and parent commits.

```bash
git commit -m 'Add note'
git cat-file -p HEAD
```

You will see:

```text
tree <tree-id>
author ...
committer ...

Add note
```

After the second commit, you will also see:

```text
parent <previous-commit-id>
```

This parent link creates the commit graph.

```text
A <- B <- C
          ^
          main
```

`main` is not the history. `main` is a movable name pointing at commit `C`.

---

## Refs Are Just Names

Branches are refs.

Common refs:

```text
refs/heads/main
refs/heads/feature/auth
refs/remotes/origin/main
refs/tags/v1.0.0
```

Inspect them:

```bash
git show-ref
git symbolic-ref HEAD
git rev-parse HEAD
git rev-parse main
```

Usually:

```text
HEAD -> refs/heads/main -> <commit-id>
```

When you commit on `main`, Git:

1. writes blobs for changed file content
2. writes trees for directory snapshots
3. writes a commit pointing at the new tree and old `HEAD`
4. moves `refs/heads/main` to the new commit

---

## HEAD Has Two Modes

### Attached HEAD

Normal branch work:

```text
HEAD -> refs/heads/main -> C
```

A new commit moves `main`.

### Detached HEAD

Directly checking out a commit:

```text
HEAD -> C
```

A new commit creates a commit, but no branch name owns it yet.

That is not dangerous by itself. It becomes risky if you leave without creating a branch.

Fix:

```bash
git switch -c experiment/from-detached
```

---

## The Index Is The Hidden Power Tool

The index is not just "staging area" in a vague sense. It is a real data structure recording:

- path
- object id for proposed content
- file mode
- conflict stages during merge conflicts

This is why Git can stage part of a file.

```text
HEAD tree      -> last committed snapshot
index          -> next commit snapshot
working tree   -> editable filesystem
```

The most important comparisons:

```bash
git diff
```

Compares working tree to index.

```bash
git diff --cached
```

Compares index to `HEAD`.

```bash
git diff HEAD
```

Compares working tree to `HEAD`, including staged and unstaged changes.

---

## What A Commit Actually Does

Think of `git commit` as:

```text
tree_id = write_tree_from_index()
commit_id = write_commit(tree_id, parent = HEAD)
move_current_branch_to(commit_id)
```

It does not commit your working tree directly.

It commits the index.

That is why this works:

```bash
echo 'A' > file.txt
git add file.txt
echo 'B' > file.txt
git commit -m 'Commit A'
```

The commit contains `A`, not `B`, because `A` was copied into the index.

---

## Reachability And Garbage Collection

An object is easy to keep if some ref can reach it.

```text
main -> C -> B -> A
```

`A`, `B`, and `C` are reachable.

If you reset:

```text
main -> B -> A

C is no longer reachable from main.
```

But `C` is usually still recoverable through the reflog for a while.

Eventually unreachable objects can be pruned by garbage collection.

Senior intuition: "lost" commits are often not deleted. They are just unnamed.

---

## The Three Questions To Ask

When confused, ask:

1. Which commit does `HEAD` resolve to?
2. Which commit does my branch ref point to?
3. What differs between `HEAD`, index, and working tree?

Commands:

```bash
git status
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git log --oneline --graph --decorate --all -20
git diff
git diff --cached
```

If those are clear, most Git problems become mechanical.

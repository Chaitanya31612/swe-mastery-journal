# A small example

```sh
# Disposable lab only; preserve current work before beginning.
git bisect start
git bisect bad HEAD
git bisect good <known-good-id>
# Run the same small regression check, then mark:
git bisect good   # or git bisect bad
# When finished:
git bisect reset
git worktree list
```
The supplied lab makes three tiny commits and a stable check. Write the failure condition before starting bisect.
## Trace the execution

Build image → create container → start main process → write to layer/volume → stop → restart or replace. Before each step, predict which bytes and process state remain.

Trace a Rails upload written locally. A replacement container starts from the image again; it does not inherit the old writable layer.

External object storage solves a different boundary from packaging.
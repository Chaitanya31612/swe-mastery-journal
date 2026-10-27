# Follow the execution

The updater queue starts with the previous state, then applies +1 three times. The next committed render gets +3. Direct values computed from one snapshot can instead request the same next value repeatedly.

For an effect subscription: setup attaches to an external source; cleanup detaches before replacement/unmount. Include the values the effect uses. A missing dependency can keep a handler tied to old values. Development Strict Mode checks can reveal missing cleanup.

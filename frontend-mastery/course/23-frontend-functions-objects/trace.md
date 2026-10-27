## Trace the execution

Trace creation → retained binding → callback invocation. Distinguish the value at registration from the value at execution. Then trace the call expression to find this.

For object lookup, check own properties first, then the prototype chain. Object.create(null) has no usual Object prototype; it also lacks methods such as hasOwnProperty. Object.hasOwn(obj,key) works without calling a method from untrusted input.

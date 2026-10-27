# One valid adaptation

Class variables can share state across related classes. Prefer explicit immutable configuration passed to objects or carefully initialized class-instance variables per subclass. Copy defaults deliberately so nested hashes are not accidentally shared.

**Explain back:** Follow the receiver, then the lookup path. What changed in the new condition? What would make your answer fail?

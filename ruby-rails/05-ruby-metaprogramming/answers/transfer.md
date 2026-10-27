# One valid adaptation

Implement respond_to_missing? consistently with the exact names method_missing supports, then call super for unsupported names. Prefer explicit generated methods if the set is known at class definition time. Test introspection and failure behavior.

**Explain back:** When? Self? Methods? Hooks? What changed in the new condition? What would make your answer fail?

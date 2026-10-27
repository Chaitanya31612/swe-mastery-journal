# One valid repair

The class method is found before included-module methods. Use a deliberate prepend wrapper that calls super, or explicit composition such as an AuditService around the action.

Check ancestors and method.owner. Do not blindly alias methods until it works.

**How to check:** owner identifies the class or module that defines the method chosen by lookup.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.
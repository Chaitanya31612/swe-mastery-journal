# The idea

Metaprogramming means code that defines or changes program behavior, often methods. Rails uses it to build readable APIs.

Start by locating the generated methods rather than assuming the behavior is unknowable.

define_method installs an instance method using a block. define_singleton_method installs one on a particular object. class_eval changes the class/module context; instance_eval changes self for a block.

String evaluation also parses code and can be dangerous with outside input. Prefer ordinary methods or explicit tables when they are clearer.

method_missing handles failed lookup. If you deliberately support dynamic methods, implement respond_to_missing? too.

Never use an arbitrary request string as a method name to call. public_send restricts visibility, but an allowlist is still needed.
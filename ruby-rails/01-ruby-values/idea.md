# The idea

A Ruby variable holds a reference to an object. Assignment copies the reference, not the whole object. If two names point to one array, changing that array is visible through both names. Reassigning one name points it somewhere else.

Only nil and false are false in a Ruby condition. Zero, an empty string, and an empty array are true. This matters when a setting can legitimately be false. settings[:enabled] || true destroys that false value. fetch(:enabled, true) uses a default only when the key is absent.

Symbols are often labels, such as :status. Strings hold text. Neither is magic security. Prefer clear names and small methods over clever one-liners. The old language book discusses Fixnum and Bignum; Ruby 2.7 presents their unified public class as Integer.

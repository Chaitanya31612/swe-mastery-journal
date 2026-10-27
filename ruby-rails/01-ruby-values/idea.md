# Start with this

A Ruby variable points to an object. Assigning it to another variable usually copies the reference, not the object.

## See the difference

```ruby
a = [1]
b = a
b << 2
# a and b both see [1, 2]

b = [9]
# b now points somewhere else. a still sees [1, 2].
```

```text
Before reassignment:   a ─┐
                         ├──> [1, 2]
                      b ─┘
After reassignment:    a ────> [1, 2]
                      b ────> [9]
```

## One Ruby rule that surprises Java developers

Only `nil` and `false` are false in a condition.

`0`, `""`, and `[]` are all true.

A setting may correctly contain `false`. `settings[:enabled] || true` loses that choice.

Use `settings.fetch(:enabled, true)` when the default should apply only if the key is missing.

## Names and values

A symbol often acts as a label: `:status`. A string holds text: `"waiting"`.

Neither one is a security check.

Older books mention `Fixnum` and `Bignum`. In Ruby 2.7, their shared public class is `Integer`.

## Remember

Ask two questions: “Did I change the object?” and “Did I point this variable at another object?”

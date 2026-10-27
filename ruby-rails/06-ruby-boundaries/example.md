# A small example

```ruby
require "json"
def read_settings(path)
  File.open(path, "r") { |file| JSON.parse(file.read) }
rescue JSON::ParserError => error
  raise ArgumentError, "settings are not valid JSON: #{error.class}"
end

require "minitest/autorun"
class SettingTest < Minitest::Test
  def test_false_is_preserved
    assert_equal false, { enabled: false }.fetch(:enabled, true)
  end
end
```

Run the supplied standalone Ruby lab in the learning journal, not in the work project. It needs only the Ruby standard library.

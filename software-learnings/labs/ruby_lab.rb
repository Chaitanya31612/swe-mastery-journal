# Run: ruby ruby_lab.rb. Uses Ruby 2.7 standard library only.
require 'minitest/autorun'

module LabelAudit
  def label
    "audit(#{super})"
  end
end
class LabTask
  prepend LabelAudit
  def label; 'task'; end
end

def forward_lab(*args, **kwargs, &block)
  target_lab(*args, **kwargs, &block)
end
def target_lab(title, urgent: false)
  result = [title, urgent]
  block_given? ? yield(result) : result
end

class RubyExecutionLab < Minitest::Test
  def test_names_share_objects_but_reassignment_is_separate
    a = []; b = a; b << 7
    assert_equal [7], a
    b = []
    assert_equal [7], a
    refute_same a, b
  end
  def test_false_setting_and_independent_default_buckets
    assert_equal false, { enabled: false }.fetch(:enabled, true)
    h = Hash.new { |hash, key| hash[key] = [] }
    h[:a] << 1
    assert_equal [], h[:b]
    refute_same h[:a], h[:b]
  end
  def test_map_and_select_have_different_shapes
    assert_equal [nil, 2], [1,2].map { |n| n if n.even? }
    assert_equal [2], [1,2].select(&:even?)
  end
  def test_prepend_lookup_and_super
    assert_equal 'audit(task)', LabTask.new.label
    assert_equal LabelAudit, LabTask.new.method(:label).owner
  end
  def test_explicit_keyword_and_block_forwarding
    assert_equal ['ship', false], forward_lab('ship', urgent: false)
    assert_equal 'ship', forward_lab('ship', urgent: true) { |result| result.first }
  end
  def test_closure_binding_is_not_frozen
    label = 'old'; reader = -> { label }; label = 'new'
    assert_equal 'new', reader.call
  end
end

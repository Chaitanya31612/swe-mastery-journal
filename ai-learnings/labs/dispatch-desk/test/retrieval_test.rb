require 'test_helper'
class RetrievalTest < ActiveSupport::TestCase
  setup do
    fixtures_for_lab
    @own=PolicyDocument.create!(tenant_id:100,title:'Dispatch',body:'Complete address before dispatch',source_version:'v1',embedding:'[0.9,0.1,0]')
    @foreign_doc=PolicyDocument.create!(tenant_id:200,title:'Forbidden',body:'Private dispatch',source_version:'v1',embedding:'[1,0,0]')
  end
  test 'exact vector search scopes before returning closest candidates' do
    rows=Ai::DocumentRetriever.call(actor:@a,query:'dispatch',vector:[1,0,0])
    assert_equal [@own.id],rows.map { |r| r[:id] }
    assert_not rows.any? { |r| r[:body].include?('Private') }
  end
  test 'lexical query scopes and attaches version' do
    rows=Ai::DocumentRetriever.call(actor:@a,query:'address')
    assert_equal 'v1',rows.first[:source_version]
  end
  test 'unpublished document is not returned' do
    @own.update!(published:false)
    assert_empty Ai::DocumentRetriever.call(actor:@a,query:'address',vector:[1,0,0])
  end
  test 'invalid dimensions and nonnumeric vectors are rejected' do
    [[1,0],['not-sql',0,1],[0,0,0]].each do |vector|
      assert_raises(Ai::InvalidResult) { Ai::DocumentRetriever.call(actor:@a,query:'address',vector:vector) }
    end
  end
end

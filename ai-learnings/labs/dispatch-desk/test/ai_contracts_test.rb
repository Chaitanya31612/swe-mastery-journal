require 'test_helper'
class AiContractsTest < ActiveSupport::TestCase
  setup { fixtures_for_lab }
  test 'filter rejects privilege fields' do
    assert_raises(Ai::InvalidResult) { Ai::Filter.parse!({'status'=>'held','tenant_id'=>200}) }
  end
  test 'filter scope cannot return another tenant' do
    filter=Ai::Filter.parse!({'status'=>'held'})
    assert_equal [@shipment.id],filter.apply(Shipment.visible_to(@a)).pluck(:id)
  end
  test 'fact builder rejects foreign record' do
    assert_raises(ActiveRecord::RecordNotFound) { Ai::FactBuilder.call(actor:@a,shipment_id:@foreign.id) }
  end
  test 'revoked actor has no visible data' do
    @a.update!(active:false)
    assert_empty Shipment.visible_to(@a)
  end
  test 'unknown field malformed output and timeout preserve manual path' do
    %w[unknown_field malformed timeout].each do |fault|
      result=Ai::IntentService.new(provider:Ai::Providers::FixtureProvider.new(fault:fault)).call(actor:@a,text:'held parcels')
      assert_equal 'unavailable',result[:state]
      assert result[:manual_path]
    end
  end
  test 'invalid citation and wrong count use reviewed fallback' do
    facts=Ai::FactBuilder.call(actor:@a,shipment_id:@shipment.id)
    %w[unknown_citation wrong_count timeout malformed].each do |fault|
      result=Ai::ExplanationService.new(provider:Ai::Providers::FixtureProvider.new(fault:fault)).call(facts:facts)
      assert_equal 'fallback',result[:state]
      assert_equal facts[:reviewed_guidance],result[:summary]
    end
  end
  test 'accepted prose remains labelled draft rather than fully verified' do
    facts=Ai::FactBuilder.call(actor:@a,shipment_id:@shipment.id)
    result=Ai::ExplanationService.new(provider:Ai::Providers::FixtureProvider.new).call(facts:facts)
    assert_equal 'AI draft - review interpretation',result[:label]
  end
  test 'fact snapshot changes after data change' do
    old=Ai::FactBuilder.call(actor:@a,shipment_id:@shipment.id)
    @shipment.update!(address_complete:true)
    current=Ai::FactBuilder.call(actor:@a,shipment_id:@shipment.id)
    assert_not_equal old[:source_version],current[:source_version]
    assert_equal 'no_supported_blocker',current[:facts].first[:reason_code]
  end
  test 'bounded agent stops endless proposals' do
    planner=->(_) {{type:'tool',name:'read_shipment_facts',arguments:{shipment_id:@shipment.id}}}
    result=Ai::BoundedAgent.new(planner:planner,tools:Ai::FactBuilder.method(:call),max_steps:2).call(actor:@a)
    assert_equal 'partial',result[:state]
    assert_equal 2,result[:observations].size
  end
  test 'bounded agent refuses unknown tools before execution' do
    planner=->(_) {{type:'tool',name:'export_all',arguments:{}}}
    tool=->(**_) { flunk 'Forbidden tool executed' }
    assert_equal 'denied',Ai::BoundedAgent.new(planner:planner,tools:tool).call(actor:@a)[:state]
  end
  test 'a stale actor object cannot preserve revoked access' do
    Actor.where(id:@a.id).update_all(active:false)
    assert @a.active? # caller still has the old in-memory object
    assert_raises(ActiveRecord::RecordNotFound) { Ai::FactBuilder.call(actor:@a,shipment_id:@shipment.id) }
  end

  test 'a bounded workflow can read facts then stop' do
    planner=->(observations) { observations.empty? ? {type:'tool',name:'read_shipment_facts',arguments:{shipment_id:@shipment.id}} : {type:'final'} }
    result=Ai::BoundedAgent.new(planner:planner,tools:Ai::FactBuilder.method(:call)).call(actor:@a)
    assert_equal 'completed',result[:state]
    assert_equal @shipment.id,result[:observations].first[:facts].first[:shipment_id]
  end
  test 'malformed proposals and arguments never execute tools' do
    [nil,{}, {type:'tool',name:'read_shipment_facts'}, {type:'tool',name:'read_shipment_facts',arguments:{shipment_id:'not-an-integer'}}].each do |proposal|
      tool=->(**_) { flunk 'Malformed proposal executed' }
      result=Ai::BoundedAgent.new(planner:->(_) {proposal},tools:tool).call(actor:@a)
      assert_equal 'denied',result[:state]
    end
  end

end

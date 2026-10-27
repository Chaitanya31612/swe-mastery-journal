require 'test_helper'
class JobsAndAdapterTest < ActiveSupport::TestCase
  setup { fixtures_for_lab }
  test 'run uses stored actor and ignores repeated completed execution' do
    run=Ai::Run.create!(actor:@a,shipment:@shipment)
    Ai::ExplainRunJob.perform_now(run.id)
    assert_equal 'completed',run.reload.state
    timestamp=run.updated_at
    Ai::ExplainRunJob.perform_now(run.id)
    assert_equal timestamp,run.reload.updated_at
  end
  test 'permission revocation before job creates unavailable state' do
    run=Ai::Run.create!(actor:@a,shipment:@shipment)
    @a.update!(active:false)
    Ai::ExplainRunJob.perform_now(run.id)
    assert_equal 'unavailable',run.reload.state
  end
  test 'provider adapter maps schema and timeout with a stubbed client' do
    capture={}
    response=Struct.new(:status,:output_text,:output).new('completed','{"status":"held","depot_name":null}',[])
    endpoint=Object.new
    endpoint.define_singleton_method(:create) { |**kwargs| capture.merge!(kwargs);response }
    client=Struct.new(:responses).new(endpoint)
    result=Ai::Providers::OpenAiProvider.new(client:client,model:'fixture-model').propose_filter(text:'held')
    assert_equal 'held',result['status']
    assert_equal true,capture.dig(:text,:format,:strict)
    assert_equal 8,capture.dig(:request_options,:timeout)
    assert_equal false,capture[:store]
  end
  test 'incomplete response is not parsed as a successful result' do
    endpoint=Object.new
    endpoint.define_singleton_method(:create) { |**_| Struct.new(:status).new('incomplete') }
    client=Struct.new(:responses).new(endpoint)
    assert_raises(Ai::InvalidResult) { Ai::Providers::OpenAiProvider.new(client:client,model:'fixture-model').propose_filter(text:'held') }
  end
  test 'provider timeout becomes an unavailable intent without a fabricated count' do
    endpoint=Object.new
    endpoint.define_singleton_method(:create) { |**_| raise OpenAI::Errors::APITimeoutError.new(url:'https://example.invalid') }
    client=Struct.new(:responses).new(endpoint)
    provider=Ai::Providers::OpenAiProvider.new(client:client,model:'fixture-model')
    result=Ai::IntentService.new(provider:provider).call(actor:@a,text:'held')
    assert_equal 'unavailable',result[:state]
    assert_not result.key?(:count)
  end
  test 'provider refusal is never treated as structured success' do
    part=Struct.new(:type).new('refusal')
    response=Struct.new(:status,:output_text,:output).new('completed','{}',[Struct.new(:content).new([part])])
    endpoint=Object.new
    endpoint.define_singleton_method(:create) { |**_| response }
    client=Struct.new(:responses).new(endpoint)
    assert_raises(Ai::InvalidResult) { Ai::Providers::OpenAiProvider.new(client:client,model:'fixture-model').propose_filter(text:'held') }
  end

end

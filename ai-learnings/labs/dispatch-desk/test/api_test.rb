require 'test_helper'
class ApiTest < ActionDispatch::IntegrationTest
  include ActiveJob::TestHelper
  setup do
    @actor=Actor.find_or_initialize_by(handle:'operator-a');@actor.update!(tenant_id:400,active:true)
    @other=Actor.find_or_initialize_by(handle:'operator-b');@other.update!(tenant_id:500,active:true)
    @shipment=Shipment.create!(title:'API synthetic',tenant_id:400,depot_name:'East Yard',status:'held',address_complete:false,label_printed:true)
    @foreign=Shipment.create!(title:'API forbidden',tenant_id:500,depot_name:'East Yard',status:'held',address_complete:false,label_printed:true)
    @headers={'X-Learning-Actor'=>'operator-a'}
  end
  test 'unauthenticated training access rejected' do
    get '/training/shipments';assert_response :unauthorized
  end
  test 'list excludes foreign records' do
    get '/training/shipments',headers:@headers
    assert_response :success
    assert_equal [@shipment.id],response.parsed_body.map { |r| r['id'] }
  end
  test 'stored result becomes stale after source update' do
    run=nil
    perform_enqueued_jobs do
      post '/training/explanations',params:{shipment_id:@shipment.id},headers:@headers,as: :json
      assert_response :accepted;run=response.parsed_body.fetch('id')
    end
    @shipment.update!(address_complete:true)
    get "/training/runs/#{run}",headers:@headers
    assert_equal 'stale',response.parsed_body['state']
  end
  test 'another actor cannot read a run result' do
    run=Ai::Run.create!(actor:@other,shipment:@foreign)
    get "/training/runs/#{run.id}",headers:@headers
    assert_response :not_found
  end
  test 'MCP HTTP rejects missing training identity and bad origin' do
    post '/mcp',params:'{}',headers:{'Content-Type'=>'application/json'}
    assert_response :unauthorized
    post '/mcp',params:'{}',headers:@headers.merge('Content-Type'=>'application/json','Origin'=>'https://untrusted.example')
    assert_response :forbidden
  end
end

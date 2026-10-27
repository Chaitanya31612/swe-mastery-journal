require 'test_helper'
class McpTest < ActiveSupport::TestCase
  setup { fixtures_for_lab }
  def call(server,method,params={},id:1)
    body={jsonrpc:'2.0',method:method,params:params};body[:id]=id if id
    raw=server.handle_json(JSON.generate(body))
    raw && !raw.empty? ? JSON.parse(raw) : nil
  end
  def initialized_server(actor)
    server=Ai::McpServer.for_actor(actor)
    result=call(server,'initialize',{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'learning-test',version:'1.0'}})
    assert result['result'],result.inspect
    call(server,'notifications/initialized',{},id:nil)
    server
  end
  test 'official SDK exposes and calls the scoped tool' do
    server=initialized_server(@a)
    tools=call(server,'tools/list')['result']['tools']
    name=tools.first.fetch('name')
    result=call(server,'tools/call',{name:name,arguments:{shipment_id:@shipment.id}})
    assert_not result['error'],result.inspect
    assert_includes result.to_json,'address_missing'
  end
  test 'official SDK rejects unknown arguments' do
    server=initialized_server(@a)
    name=call(server,'tools/list')['result']['tools'].first['name']
    result=call(server,'tools/call',{name:name,arguments:{shipment_id:@shipment.id,tenant_id:200}})
    assert result['error'] || result.dig('result','isError'),result.inspect
  end
  test 'foreign record is unavailable through SDK' do
    server=initialized_server(@a)
    name=call(server,'tools/list')['result']['tools'].first['name']
    result=call(server,'tools/call',{name:name,arguments:{shipment_id:@foreign.id}})
    assert_not_includes result.to_json,@foreign.title
    assert_not result['error'],result.inspect
    assert_equal true,result.dig('result','isError')
    assert_includes result.to_json,'Access or source unavailable'
  end
end

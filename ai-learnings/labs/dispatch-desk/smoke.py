"""Synthetic live HTTP + official MCP transport checks. No provider calls."""
import json,time,urllib.request
BASE='http://127.0.0.1:3310'
def request(path,body=None,actor='operator-a',extra=None):
    headers={'X-Learning-Actor':actor,'Content-Type':'application/json'};headers.update(extra or {})
    req=urllib.request.Request(BASE+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
    with urllib.request.urlopen(req,timeout=10) as r:
        raw=r.read().decode();return json.loads(raw) if raw else None
rows=request('/training/shipments');assert rows
id=rows[0]['id']
assert request('/training/intent',{'text':'held','fault':'unknown_field'})['state']=='unavailable'
run=request('/training/explanations',{'shipment_id':id,'fault':'unknown_citation'})
for _ in range(40):
    result=request('/training/runs/'+str(run['id']))
    if result['state'] not in ['queued','running']:break
    time.sleep(.1)
assert result['state']=='fallback',result
print('PASS: live scoped query, rejected intent, asynchronous invalid-citation fallback')
headers={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
def rpc(method,params,id=1):
    body={'jsonrpc':'2.0','method':method,'params':params}
    if id is not None:body['id']=id
    return request('/mcp',body,extra=headers)
assert rpc('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'learning-smoke','version':'1'}})['result']
rpc('notifications/initialized',{},None)
tools=rpc('tools/list',{})['result']['tools'];name=tools[0]['name']
result=rpc('tools/call',{'name':name,'arguments':{'shipment_id':id}})
assert not result.get('error'),result
assert 'address_missing' in json.dumps(result) or 'label_missing' in json.dumps(result),result
print('PASS: initialized local HTTP MCP lifecycle, discovery, and real SDK tool result')

foreign=request('/training/shipments',actor='operator-b')[0]['id']
denied=rpc('tools/call',{'name':name,'arguments':{'shipment_id':foreign}})
assert not denied.get('error'),denied
assert denied['result']['isError'] is True,denied
assert 'Access or source unavailable' in json.dumps(denied)
assert 'Synthetic foreign parcel' not in json.dumps(denied)
print('PASS: HTTP MCP call cannot cross the current actor scope')

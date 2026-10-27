"""Live synthetic check. Run beside compose.yaml after compose up."""
import json, subprocess, time, urllib.request

def rails(code):
    result=subprocess.run(['docker','compose','exec','-T','web','bundle','exec','rails','runner',code],check=True,capture_output=True,text=True)
    return next(line[7:] for line in result.stdout.splitlines() if line.startswith('RESULT:'))

def wait_projection(ticket_id):
    for _ in range(80):
        with urllib.request.urlopen('http://127.0.0.1:3300/tickets/'+str(ticket_id)) as response:
            result=json.load(response)
        if result['projection_count']==1:return
        time.sleep(0.5)
    raise AssertionError('Projection did not catch up: '+str(ticket_id))

def complete(ticket_id):
    req=urllib.request.Request('http://127.0.0.1:3300/tickets/'+str(ticket_id)+'/complete',data=b'',method='POST')
    with urllib.request.urlopen(req) as response:assert response.status==200

ticket_id=int(rails("puts 'RESULT:'+Ticket.create!(title: 'Live synthetic smoke').id.to_s"))
complete(ticket_id);complete(ticket_id);wait_projection(ticket_id)
assert rails(f"puts 'RESULT:'+OutboxEvent.where(aggregate_key: '{ticket_id}').count.to_s")=='1'
rails(f"p=KafkaPublisher.new; e=OutboxEvent.find_by!(aggregate_key: '{ticket_id}'); p.publish(e.envelope,key:e.aggregate_key);p.close;puts 'RESULT:sent'")
time.sleep(2)
assert rails(f"puts 'RESULT:'+ReportingProjection.find_by!(ticket_id: {ticket_id}).completed_count.to_s")=='1'
print('PASS: live delivery, command repeat, delivery repeat; effect count = 1')
subprocess.run(['docker','compose','stop','consumer'],check=True)
try:
    second=int(rails("puts 'RESULT:'+Ticket.create!(title: 'Catch-up smoke').id.to_s"))
    complete(second)
    for _ in range(40):
        if rails(f"puts 'RESULT:'+OutboxEvent.where(aggregate_key: '{second}').where.not(published_at:nil).count.to_s")=='1':break
        time.sleep(0.5)
    else:raise AssertionError('Dispatcher did not publish')
    assert rails(f"puts 'RESULT:'+ReportingProjection.where(ticket_id: {second}).count.to_s")=='0'
finally:
    subprocess.run(['docker','compose','start','consumer'],check=True)
wait_projection(second)
print('PASS: record persisted while consumer stopped; projection caught up on restart')

"""Small RESP client + real Redis checks. Python standard library only.
Uses a fresh key prefix; never FLUSHALL/FLUSHDB. Requires this lab's Redis.
"""
import socket, time, uuid
from concurrent.futures import ThreadPoolExecutor
PREFIX = 'learning:' + uuid.uuid4().hex + ':'

class Redis:
    def __enter__(self):
        self.socket = socket.create_connection(('127.0.0.1', 16379), timeout=3)
        self.file = self.socket.makefile('rb')
        return self
    def __exit__(self, *_):
        self.file.close(); self.socket.close()
    def command(self, *parts):
        args = [str(p).encode() for p in parts]
        wire = b'*'+str(len(args)).encode()+b'\r\n'
        for arg in args: wire += b'$'+str(len(arg)).encode()+b'\r\n'+arg+b'\r\n'
        self.socket.sendall(wire)
        return self.read()
    def read(self):
        line = self.file.readline()
        if not line: raise ConnectionError('Redis closed connection')
        kind, data = line[:1], line[1:-2]
        if kind == b'+': return data.decode()
        if kind == b'-': raise RuntimeError(data.decode())
        if kind == b':': return int(data)
        size = int(data)
        if size == -1: return None
        if kind == b'$':
            value = self.file.read(size); self.file.read(2); return value.decode()
        if kind == b'*': return [self.read() for _ in range(size)]
        raise ValueError('Unexpected RESP type')

def key(name): return PREFIX+name

def increment(_):
    with Redis() as r:
        for _ in range(100): r.command('INCR', key('count'))

with Redis() as r:
    assert r.command('PING') == 'PONG'
    r.command('HSET', key('ticket'), 'status', 'open', 'owner', '12')
    assert r.command('HGET', key('ticket'), 'status') == 'open'
    r.command('ZADD', key('rank'), 40, 'a', 90, 'b', 75, 'c')
    assert r.command('ZREVRANGE', key('rank'), 0, 1) == ['b', 'c']
    print('PASS: hashes and sorted-set ordering')

with ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(increment, range(8)))
with Redis() as r:
    assert r.command('GET', key('count')) == '800'
    # Atomic command does not imply arbitrary multi-command workflows are atomic.
    both_read = r.command('GET', key('count'))
    r.command('SET', key('count'), int(both_read)+1)
    r.command('SET', key('count'), int(both_read)+1)
    assert r.command('GET', key('count')) == '801' # expected lost update
    print('PASS: INCR preserves concurrent increments; GET/SET loses a modeled update')

    assert r.command('SET', key('lease'), 'A', 'NX', 'PX', 80) == 'OK'
    deadline = time.monotonic()+3
    while r.command('GET', key('lease')) is not None:
        assert time.monotonic()<deadline
        time.sleep(.01)
    assert r.command('SET', key('lease'), 'B', 'NX', 'PX', 5000) == 'OK'
    release = "if redis.call('get',KEYS[1]) == ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end"
    assert r.command('EVAL', release, 1, key('lease'), 'A') == 0
    assert r.command('GET', key('lease')) == 'B'
    assert r.command('EVAL', release, 1, key('lease'), 'B') == 1
    print('PASS: expired owner cannot release replacement lease')

    window = "local n=redis.call('incr',KEYS[1]); if n==1 then redis.call('pexpire',KEYS[1],ARGV[1]) end; return n"
    assert r.command('EVAL', window, 1, key('window'), 10000) == 1
    assert r.command('EVAL', window, 1, key('window'), 10000) == 2
    assert 0 < r.command('PTTL', key('window')) <= 10000
    print('PASS: counter and first expiry execute together in Lua')

    r.command('XADD', key('stream'), '*', 'event_id', 'synthetic-e1')
    r.command('XGROUP', 'CREATE', key('stream'), 'reporting', '0')
    records = r.command('XREADGROUP', 'GROUP', 'reporting', 'worker-a', 'COUNT', 1, 'STREAMS', key('stream'), '>')
    record_id = records[0][1][0][0]
    assert r.command('XPENDING', key('stream'), 'reporting')[0] == 1
    assert r.command('XACK', key('stream'), 'reporting', record_id) == 1
    assert r.command('XPENDING', key('stream'), 'reporting')[0] == 0
    assert r.command('XLEN', key('stream')) == 1
    print('PASS: stream acknowledgment clears pending state; retained record remains')
    r.command('DEL', *[key(x) for x in ['ticket','rank','count','lease','window','stream']])
print('All synthetic Redis checks passed; this run removed only its own keys.')

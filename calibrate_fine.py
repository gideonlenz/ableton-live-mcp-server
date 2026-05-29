import socket, json, time

def send(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'x', 'method': 'send_message',
                      'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(0.4)
    try:
        data = s.recv(65536)
        s.close()
        return json.loads(data.decode())
    except:
        s.close()
        return {}

def sp(idx, val, name):
    r = send('/live/device/set/parameter/value', [1, 0, idx, val])
    st = r.get('result', {}).get('status', '?')
    r2 = send('/live/device/get/parameter/value_string', [1, 0, idx])
    sv = r2.get('result', {}).get('data', ['','','','?'])
    display = sv[-1] if sv else '?'
    print("  [%d] %-25s = %s -> %s  (display: %s)" % (idx, name, val, st, display))

print("=== Calibrating Fine detune (range 0-1000) ===")
print()

# Test with 500 first to find center
sp(14, 500.0, "A Fine test 500")
sp(41, 500.0, "B Fine test 500")
time.sleep(0.3)

print()
print("=== Reading back values and strings ===")
for idx, name in [(14,"A Fine"), (41,"B Fine")]:
    rv = send('/live/device/get/parameter/value', [1, 0, idx])
    vd = rv.get('result', {}).get('data', [])
    rs = send('/live/device/get/parameter/value_string', [1, 0, idx])
    sd = rs.get('result', {}).get('data', [])
    val = vd[-1] if vd else '?'
    sval = sd[-1] if sd else '?'
    print("  %s: value=%s, display='%s'" % (name, val, sval))

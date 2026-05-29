import socket, json, time

def send_osc_raw(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'test', 'method': 'send_message', 'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(2.0)
    try:
        data = s.recv(131072)
        s.close()
        return json.loads(data.decode())
    except Exception as e:
        s.close()
        return {'error': str(e)}

print('Getting ALL parameter min values...')
r = send_osc_raw('/live/device/get/parameters/min', [1, 0])
data = r.get('result', {}).get('data', [])
mins = data[2:]

print('Getting ALL parameter max values...')
r2 = send_osc_raw('/live/device/get/parameters/max', [1, 0])
data2 = r2.get('result', {}).get('data', [])
maxs = data2[2:]

print('Getting ALL parameter current values...')
r3 = send_osc_raw('/live/device/get/parameters/value', [1, 0])
data3 = r3.get('result', {}).get('data', [])
vals = data3[2:]

print('Getting ALL parameter names...')
r4 = send_osc_raw('/live/device/get/parameters/name', [1, 0])
data4 = r4.get('result', {}).get('data', [])
names = data4[2:]

key_params = [1,4,8,12,13,20,25,29,31,33,34,39,40,47,52,56,58,60,61,66,93,165,166,170,171,173,176,178,181,184]

print()
print("Idx   Name                      Min        Max    Current")
print('-' * 65)
for i in key_params:
    if i < len(names):
        n = str(names[i]) if i < len(names) else '?'
        mn = str(mins[i]) if i < len(mins) else '?'
        mx = str(maxs[i]) if i < len(maxs) else '?'
        v = vals[i] if i < len(vals) else '?'
        if isinstance(v, float):
            v = str(round(v, 4))
        else:
            v = str(v)
        print(f"{i:>4}  {n:<25} {mn:>10} {mx:>10} {v:>10}")

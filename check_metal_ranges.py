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

r = send_osc_raw('/live/device/get/parameters/min', [1, 0])
mins = r.get('result', {}).get('data', [])[2:]

r2 = send_osc_raw('/live/device/get/parameters/max', [1, 0])
maxs = r2.get('result', {}).get('data', [])[2:]

r3 = send_osc_raw('/live/device/get/parameters/name', [1, 0])
names = r3.get('result', {}).get('data', [])[2:]

# Print all params we need for metallic lead
metal_params = [
    1,                        # Algorithm
    26, 53, 80, 107,          # Feedback A,B,C,D
    120, 121,                 # Time, Time<Key
    122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,  # Pitch Envelope
    141,142,143,144,145,146,147,148,149,150,151,152,153,  # LFO
    192,193,194               # Shaper
]

print("Idx   Name                      Min        Max")
print('-' * 55)
for i in metal_params:
    if i < len(names):
        n = str(names[i])
        mn = str(mins[i]) if i < len(mins) else '?'
        mx = str(maxs[i]) if i < len(maxs) else '?'
        print(f"{i:>4}  {n:<25} {mn:>10} {mx:>10}")

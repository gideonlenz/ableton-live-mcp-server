import socket, json, time

def send(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'x', 'method': 'send_message',
                      'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(0.5)
    try:
        data = s.recv(65536)
        s.close()
        return json.loads(data.decode())
    except:
        s.close()
        return {}

def sp(idx, val):
    send('/live/device/set/parameter/value', [1, 0, idx, val])

def gstr(idx):
    r = send('/live/device/get/parameter/value_string', [1, 0, idx])
    d = r.get('result', {}).get('data', [])
    return d[-1] if d else '?'

def gval(idx):
    r = send('/live/device/get/parameter/value', [1, 0, idx])
    d = r.get('result', {}).get('data', [])
    return d[-1] if d else '?'

# Probe A Fine at various values to understand the scale
print("=== Probing A Fine (param 14) at different values ===")
print("(Range: 0-1000, trying to find what 0, 500, 1000 map to in cents)")
print()

test_vals = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for v in test_vals:
    sp(14, float(v))
    time.sleep(0.1)
    s = gstr(14)
    actual = gval(14)
    print("  value=%-6s  ->  actual=%-8s  display='%s'" % (v, actual, s))

# Reset to 0
sp(14, 0.0)
print()

# Based on the display values, determine: 
# If display is in semitones (0-1000 = 0-100.0 semitones = 0 to +100st)
# OR if 0-1000 maps to 0-100 cents (centitones)
# Operator Fine in UI shows -50 to +50 cents
# So likely: 500=0ct, 0=-50ct, 1000=+50ct
# OR: 0=0, 1000=100 (raw cent value * 10)

# Apply AFX microtonal Fine detune now that we understand the scale
# If 0=0ct and 1000=100ct (0 to +100 cents semitone range):
#   +7 cents = 70, +15 cents = 150, -8 cents = ??? (might not go negative)
# If 500=0ct (center) and range is -50 to +50:
#   +7ct = 570, -8ct = 430, +15ct = 650, -16ct = 340

print("=== Applying microtonal Fine detuning ===")
print("Assuming 500=0 cents, range is -50ct to +50ct:")
print()

# Each oscillator slightly detuned in different directions
# Creates beating and that characteristic AFX 'not-quite-in-tune' shimmer
# A: +7 cents  -> 500 + 70 = 570
# B: -8 cents  -> 500 - 80 = 420
# C: +15 cents -> 500 + 150 = 650  (near quarter tone!)
# D: -16 cents -> 500 - 160 = 340  (pulling down hard)

detune_map = [
    (14, 570.0, "A Fine +7 cents"),
    (41, 420.0, "B Fine -8 cents"),
    (68, 650.0, "C Fine +15 cents (near quarter-tone)"),
    (95, 340.0, "D Fine -16 cents (lowest mod pulls down)"),
]

for idx, val, name in detune_map:
    sp(idx, val)
    time.sleep(0.15)
    s = gstr(idx)
    print("  [%d] %-38s = %s  (display: %s)" % (idx, name, val, s))

print()
print("AFX Microtonal detuning applied!")
print("Each oscillator is now at a slightly different pitch center.")
print("This creates the characteristic beating/shimmer of AFX/RDJ sounds.")

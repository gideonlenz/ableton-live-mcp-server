import socket, json, time

def send_osc(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'patch', 'method': 'send_message', 'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(0.35)
    try:
        data = s.recv(65536)
        s.close()
        return json.loads(data.decode())
    except Exception as e:
        s.close()
        return {'error': str(e)}

def set_param(param_idx, value, name=""):
    r = send_osc('/live/device/set/parameter/value', [1, 0, param_idx, value])
    status = r.get('result', {}).get('status', 'unknown')
    print(f"  [{param_idx:3d}] {name:<25} = {value} -> {status}")
    return status

def read_param(param_idx):
    r = send_osc('/live/device/get/parameter/value', [1, 0, param_idx])
    data = r.get('result', {}).get('data', [])
    return data[-1] if data else None

print("=== GD Luxxe Electro Bass - CORRECTED PATCH ===")
print("(All 0-1 normalized params use 0.0-1.0 range)")
print()

# --- ALGORITHM: index 1, range 0-10 ---
# Algorithm 1 = B->A (modulator->carrier) classic FM
set_param(1, 1.0, "Algorithm (B->A)")

# --- OSC A: Carrier, Sine, full level ---
set_param(12, 1.0, "Osc-A On")
set_param(13, 1.0, "A Coarse (x1)")       # range 0-48, value 1 = 1x ratio
set_param(20, 1.0, "Osc-A Level")          # range 0-1, 1.0 = max
set_param(25, 0.0, "Osc-A Wave (Sine)")    # range 0-22, 0 = sine

# --- OSC A Envelope: snappy pluck ---
# Range is 0-1 (internally mapped to ms by Ableton)
# ~0.0 = near 0ms, ~0.1 = ~8ms, ~0.5 = ~150ms, ~0.63 = ~300ms, ~0.75 = ~1s
set_param(29, 0.0,  "Ae Attack (~0ms)")     # instant attack
set_param(31, 0.55, "Ae Decay (~200ms)")    # snappy decay
set_param(33, 0.0,  "Ae Sustain (0)")       # no sustain = pluck
set_param(34, 0.45, "Ae Release (~80ms)")   # quick release

# --- OSC B: Modulator for FM growl ---
set_param(39, 1.0, "Osc-B On")
set_param(40, 2.0, "B Coarse (x2)")        # 2x ratio = classic FM bass growl
set_param(47, 0.65, "Osc-B Level (mod depth)") # 0-1, 0.65 = good growl
set_param(52, 0.0, "Osc-B Wave (Sine)")

# --- OSC B Envelope: fast mod falloff ---
set_param(56, 0.0,  "Be Attack (~0ms)")
set_param(58, 0.42, "Be Decay (~60ms)")    # fast FM falloff = transient click
set_param(60, 0.0,  "Be Sustain (0)")
set_param(61, 0.35, "Be Release (~30ms)")

# --- OSC C and D OFF ---
set_param(66, 0.0, "Osc-C Off")
set_param(93, 0.0, "Osc-D Off")

# --- FILTER: Low-pass warm electro ---
set_param(165, 1.0, "Filter On")
set_param(166, 0.0, "Filter Type (LP)")    # 0-4, 0 = LP
# Filter Freq: 0-1 normalized. ~0.55 = ~1kHz, ~0.65 = ~2kHz, ~0.72 = ~4kHz
set_param(170, 0.68, "Filter Freq (~3kHz)")
# Filter Res: range 0-1.25
set_param(171, 0.18, "Filter Res (subtle)")
# Filter Drive: range 0-24 (actual dB)
set_param(173, 8.0, "Filter Drive (8dB)")

# --- FILTER ENVELOPE ---
# Fe Amount: range -100 to 100
set_param(176, 40.0, "Fe Amount (40)")
# Fe Attack/Decay: 0-1 normalized
set_param(178, 0.0,  "Fe Attack (~0ms)")
set_param(181, 0.48, "Fe Decay (~100ms)")
set_param(184, 0.0,  "Fe Sustain (0)")

# --- VOLUME & TONE ---
# Volume: 0-1 normalized
set_param(4, 0.85, "Volume (0.85)")
# Tone: 0-1
set_param(8, 0.5,  "Tone (0.5)")

print()
print("=== Verifying key params ===")
checks = [(1,"Algorithm"), (20,"Osc-A Level"), (47,"Osc-B Level"), (170,"Filter Freq"), (173,"Filter Drive")]
for idx, name in checks:
    v = read_param(idx)
    print(f"  [{idx:3d}] {name:<20} = {v}")

print()
print("=== PATCH COMPLETE - Check Operator in Ableton! ===")

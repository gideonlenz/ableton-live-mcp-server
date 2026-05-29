import socket, json, time

TRACK = 1  # Operator Riff track
DEVICE = 0
CLIP_SLOT = 0

def send(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'afx', 'method': 'send_message',
                      'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(6)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(0.38)
    try:
        data = s.recv(131072)
        s.close()
        return json.loads(data.decode())
    except Exception as e:
        s.close()
        return {'error': str(e)}

def sp(idx, val, name=""):
    r = send('/live/device/set/parameter/value', [TRACK, DEVICE, idx, val])
    st = r.get('result', {}).get('status', '?')
    print(f"  [{idx:3d}] {name:<32} = {val:<8} -> {st}")

def rp(idx):
    r = send('/live/device/get/parameter/value', [TRACK, DEVICE, idx])
    return r.get('result', {}).get('data', [None])[-1]

# ============================================================
print("=" * 62)
print("  AFX TWIN MICROTONAL SOUND DESIGN")
print("  Algorithm 5: Full FM chain D->C->B->A")
print("  Character: Atonal, microtonal, evolving, complex")
print("=" * 62)
print()

# ALGORITHM 5 = D->C->B->A full linear chain
# Maximum FM complexity - each op modulates the one below it
# D modulates C, C modulates B, B modulates A (output carrier)
sp(1, 5.0, "Algorithm (D->C->B->A chain)")

# --- OSC A: Carrier (output) ---
# Slightly detuned for microtonal quality
# Fine range: 0-1 where 0.5 = center (0 cents), so:
# 0.52 = slightly sharp (~4 cents) - just enough to feel 'off'
sp(12, 1.0, "Osc-A On")
sp(13, 1.0, "A Coarse (x1)")
sp(14, 0.52, "A Fine (+~4 cents, microtonal!)")   # slightly sharp
sp(20, 1.0,  "Osc-A Level")
sp(25, 0.0,  "Osc-A Wave (Sine)")
sp(26, 18.0, "Osc-A Feedb (self-FM grit)")        # 0-100, 18 = AFX-style partial distortion

# OSC A Envelope: slow attack - AFX pads have slow bloom
sp(29, 0.25, "Ae Attack (slow ~20ms bloom)")
sp(31, 0.80, "Ae Decay (long, >2s)")
sp(33, 0.65, "Ae Sustain (65% = held)")
sp(34, 0.75, "Ae Release (~1s long)")

# --- OSC B: Modulator 3rd in chain ---
# Ratio 2, but fine-detuned to create beating/microtonality
sp(39, 1.0,  "Osc-B On")
sp(40, 2.0,  "B Coarse (x2)")
sp(41, 0.45, "B Fine (-~8 cents, microtonal!)")   # slightly flat of x2
sp(47, 0.72, "Osc-B Level (strong mod)")
sp(52, 0.0,  "Osc-B Wave (Sine)")
sp(53, 35.0, "Osc-B Feedb (AFX chaos!)")          # 0-100, 35 = significant self-FM

# OSC B Envelope: medium - feeds modulation throughout note
sp(56, 0.0,  "Be Attack (instant)")
sp(58, 0.88, "Be Decay (very long ~5s)")           # long mod sustain = evolving
sp(60, 0.45, "Be Sustain (45% mod held)")
sp(61, 0.70, "Be Release")

# --- OSC C: Modulator 2nd in chain ---
# Ratio 5 (or odd prime for atonal complexity)
sp(66, 1.0,  "Osc-C On")
sp(67, 5.0,  "C Coarse (x5 inharmonic)")
sp(68, 0.55, "C Fine (+~8 cents, quarter-tone flavor)") # slightly sharp of x5
sp(74, 0.55, "Osc-C Level")
sp(79, 0.0,  "Osc-C Wave (Sine)")
sp(80, 20.0, "Osc-C Feedb (partial self-FM)")     # 0-100

# OSC C Envelope: starts full, very slowly decays (keeps evolving)
sp(83, 0.0,  "Ce Attack (instant)")
sp(85, 0.92, "Ce Decay (extremely long ~10s)")
sp(87, 0.60, "Ce Sustain (60% mod)")
sp(88, 0.80, "Ce Release")

# --- OSC D: Deepest modulator - the chaos source ---
# Ratio 7 (prime, highly inharmonic) + large fine detune
sp(93,  1.0,  "Osc-D On")
sp(94,  7.0,  "D Coarse (x7 prime = atonal)")
sp(95,  0.42, "D Fine (-~16 cents!) deep microtonal")  # notably flat = beating
sp(101, 0.48, "Osc-D Level (controlled chaos)")
sp(106, 0.0,  "Osc-D Wave (Sine - pure FM)")
sp(107, 45.0, "Osc-D Feedb (heavy! AFX character)") # 0-100, 45 = Richard D. James level

# OSC D Envelope: slow attack on deepest mod = delayed chaos burst
sp(110, 0.18, "De Attack (slow, chaos builds...)")
sp(112, 0.95, "De Decay (almost infinite)")
sp(114, 0.55, "De Sustain (55%)")
sp(115, 0.85, "De Release (very long fade)")

print()

# --- PITCH ENVELOPE: subtle pitch drift ---
# AFX sounds often have slight pitch movement at attack
sp(122, 1.0,  "Pe On")
sp(123, 0.0,  "Pe Attack (instant pitch hit)")
sp(124, 5.0,  "Pe Init (+5 semitones)")           # small pitch jump up
sp(125, -0.5, "Pe A Slope (exponential)")          # curved
sp(126, 0.45, "Pe Decay (~90ms)")                  # quick fall to root
sp(127, 0.0,  "Pe Peak (settle at root)")
sp(129, 0.0,  "Pe Sustain")
sp(137, 0.35, "Pe Amount (35% = subtle)")

print()

# --- LFO: Complex slow modulation ---
# Two LFO destinations: filter freq (primary) + pitch of A (secondary)
sp(141, 1.0,  "LFO On")
sp(142, 0.0,  "LFO Type (Sine)")
sp(143, 0.0,  "LFO Range (Low = ultra slow)")
sp(144, 8.0,  "LFO Rate (very slow, 0-127)")       # very slow sweep
sp(145, 0.0,  "LFO Sync (free running)")
sp(147, 0.0,  "LFO Retrigger OFF (free = evolving)")  # no retrig = drifts freely
sp(148, 0.55, "LFO Amt (filter modulation 55%)")
sp(149, 12.0, "LFO Amt A (micro pitch drift)")     # -100 to 100, 12 = subtle vibrato drift

print()

# --- FILTER: resonant, dark, slowly opening ---
sp(165, 1.0,  "Filter On")
sp(166, 0.0,  "Filter Type (LP)")
sp(167, 2.0,  "Filter Circuit LP/HP")              # 0-? different circuit character
sp(170, 0.45, "Filter Freq (~800Hz, dark)")        # 0-1, 0.45 = quite dark
sp(171, 0.65, "Filter Res (resonant, 0-1.25)")     # high resonance = AFX character
sp(173, 10.0, "Filter Drive (10dB saturation)")    # 0-24
sp(174, 30.0, "Filt < Vel (velocity opens filter)") # CHECK range later

# Filter envelope: very slow open - the "evolving" quality
sp(176, 70.0, "Fe Amount (+70 = opens wide)")
sp(178, 0.35, "Fe Attack (~40ms)")
sp(181, 0.90, "Fe Decay (very slow >5s evolve!)")  # THIS is the evolving character
sp(184, 0.40, "Fe Sustain (40% open)")
sp(185, 0.78, "Fe Release (long)")

print()

# --- SHAPER: AFX loves distorted FM ---
sp(192, 1.0,  "Shaper Type (Soft Saturate)")
sp(193, 50.0, "Shaper Mix (50% wet)")              # 0-100
sp(194, 6.0,  "Shaper Drive (+6dB)")               # -12 to 12

# Global
sp(4, 0.78,  "Volume")
sp(8, 0.55,  "Tone")
sp(9, 0.25,  "Spread (stereo width)")

print()
print("=" * 62)
print("  VERIFYING AFX PATCH...")
print("=" * 62)

checks = [
    (1,   "Algorithm (expect 5)"),
    (14,  "A Fine (microtonal)"),
    (41,  "B Fine (microtonal)"),
    (53,  "Osc-B Feedb (expect 35)"),
    (94,  "D Coarse (expect 7)"),
    (107, "Osc-D Feedb (expect 45)"),
    (141, "LFO On"),
    (170, "Filter Freq (expect 0.45)"),
    (171, "Filter Res"),
    (181, "Fe Decay (expect 0.90)"),
]
for idx, name in checks:
    v = rp(idx)
    print(f"  [{idx:3d}] {name:<35} = {v}")

print()
print("AFX SOUND PATCH COMPLETE")

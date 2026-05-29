import socket, json, time

def send_osc(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'metal', 'method': 'send_message', 'params': {'address': address, 'args': args}})
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

def set_param(idx, value, name=""):
    r = send_osc('/live/device/set/parameter/value', [1, 0, idx, value])
    status = r.get('result', {}).get('status', '?')
    print(f"  [{idx:3d}] {name:<28} = {value:<8} -> {status}")

def read_param(idx):
    r = send_osc('/live/device/get/parameter/value', [1, 0, idx])
    return r.get('result', {}).get('data', [None])[-1]

print("=" * 60)
print("  METALLIC EVOLVING LEAD — Operator Patch")
print("  Algorithm: 4 (B,C -> A carrier; D independent carrier)")
print("  Character: Inharmonic FM + Pitch Env transient + LFO sweep")
print("=" * 60)
print()

# ── ALGORITHM ───────────────────────────────────────────────
# Algorithm 4: B→A, C→A (two mods into one carrier) + D carrier
# This gives complex inharmonic overtones = metallic character
set_param(1, 4.0, "Algorithm (B,C->A + D)")

# ── OSC A: Main Carrier (fundamental) ───────────────────────
set_param(12, 1.0, "Osc-A On")
set_param(13, 1.0, "A Coarse (x1 fundamental)")   # ratio 1 = fundamental
set_param(14, 0.0, "A Fine (0 = no detune)")
set_param(20, 1.0, "Osc-A Level")
set_param(25, 0.0, "Osc-A Wave (Sine)")
set_param(26, 12.0,"Osc-A Feedb (slight self-FM)")  # range 0-100, 12 = subtle grit

# OSC A Envelope: medium attack, long sustain for lead
set_param(29, 0.05,  "Ae Attack (~3ms)")
set_param(31, 0.60,  "Ae Decay (~300ms)")
set_param(33, 0.55,  "Ae Sustain (55%)")            # held sustain for lead
set_param(34, 0.65,  "Ae Release (~500ms)")

# ── OSC B: Modulator 1 — HIGH inharmonic ratio (metallic) ───
# Ratio 7 = inharmonic overtone -> bell/metallic character
set_param(39, 1.0, "Osc-B On")
set_param(40, 7.0, "B Coarse (x7 inharmonic!)")
set_param(41, 0.0, "B Fine")
set_param(47, 0.68,"Osc-B Level (mod depth)")       # 0-1, 0.68 = strong FM
set_param(52, 0.0, "Osc-B Wave (Sine)")
set_param(53, 0.0, "Osc-B Feedb (clean)")

# OSC B Env: fast attack, fast decay -> click/transient metallic zing
set_param(56, 0.0,  "Be Attack (instant)")
set_param(58, 0.38, "Be Decay (~45ms fast!)")
set_param(60, 0.0,  "Be Sustain (0 = pluck mod)")
set_param(61, 0.28, "Be Release (~15ms)")

# ── OSC C: Modulator 2 — HIGHER inharmonic for shimmer ──────
# Ratio 11 = another inharmonic partial, adds shimmer on top
set_param(66, 1.0, "Osc-C On")
set_param(67, 11.0,"C Coarse (x11 shimmer)")
set_param(68, 0.0, "C Fine")
set_param(74, 0.38,"Osc-C Level (lighter mod depth)")  # softer, just shimmer
set_param(79, 0.0, "Osc-C Wave (Sine)")
set_param(80, 0.0, "Osc-C Feedb")

# OSC C Env: even faster decay for bright attack transient only
set_param(83, 0.0,  "Ce Attack (instant)")
set_param(85, 0.28, "Ce Decay (~18ms)")
set_param(87, 0.0,  "Ce Sustain (0)")
set_param(88, 0.20, "Ce Release")

# ── OSC D: Sub/Body Carrier — adds warmth beneath the metal ─
# D is an independent carrier (algorithm 4), ratio 0.5 = sub octave
# Coarse 0 in Operator = 0 semitones above base (still x1 in most algs)
# Use coarse=0 (will play at ratio 1 same as A) but detune for thickness
set_param(93,  1.0,  "Osc-D On")
set_param(94,  1.0,  "D Coarse (x1 = unison body)")
set_param(95,  0.52, "D Fine (slight detune +cent)")  # 0.5=0 cents, 0.52=slightly sharp
set_param(101, 0.35, "Osc-D Level (body/warmth)")
set_param(106, 3.0,  "Osc-D Wave (Square = harmonics)")  # Square adds body harmonics
set_param(107, 0.0,  "Osc-D Feedb")

set_param(110, 0.08, "De Attack (~6ms)")
set_param(112, 0.65, "De Decay (~450ms)")
set_param(114, 0.40, "De Sustain (40%)")
set_param(115, 0.60, "De Release (~350ms)")

print()

# ── PITCH ENVELOPE — signature metallic transient zing ──────
# Pe Init/Peak are in SEMITONES (-48 to 48)
# Fast pitch dive from +12st down to 0 = classic synth metallic attack
set_param(122, 1.0,  "Pe On")
set_param(123, 0.0,  "Pe Attack (instant)")
set_param(124, 12.0, "Pe Init (+12 semitones start)")   # starts 1 octave up
set_param(125, 0.5,  "Pe A Slope (linear)")
set_param(126, 0.30, "Pe Decay (~25ms fast fall)")      # falls to 0 quickly
set_param(127, 0.0,  "Pe Peak (0 = falls to root)")
set_param(129, 0.0,  "Pe Sustain (root pitch)")
set_param(137, 1.0,  "Pe Amount (full = -1 to 1, use 1.0)")

print()

# ── LFO — slow filter sweep for "evolving" character ────────
# LFO Rate range: 0-127. Low values = very slow.
# We want a slow gentle sweep, not vibrato
set_param(141, 1.0,  "LFO On")
set_param(142, 0.0,  "LFO Type (Sine)")
set_param(143, 0.0,  "LFO Range (Low = slow)")          # 0=Low range
set_param(144, 18.0, "LFO Rate (slow ~0.14Hz)")         # 0-127, 18 = gentle slow
set_param(147, 1.0,  "LFO Retrigger (fresh each note)")
set_param(148, 0.40, "LFO Amt (to filter freq)")        # 0-1, mod filter

# Set LFO destination B to filter freq for filter sweep
# Dst B 0-23, need to know filter freq destination index
# Common: 0=Pitch, 1=OscA Pitch, ... filter is usually around 10-14
# Set Amt A to pitch for subtle vibrato
set_param(149, 8.0,  "LFO Amt A (subtle pitch vibrato)") # -100 to 100, 8 = tiny

print()

# ── FILTER — LP with resonance to focus the harmonics ───────
set_param(165, 1.0,  "Filter On")
set_param(166, 0.0,  "Filter Type (LP)")
set_param(170, 0.62, "Filter Freq (~2kHz)")               # 0-1 normalized
set_param(171, 0.45, "Filter Res (resonant peak)")         # 0-1.25
set_param(173, 6.0,  "Filter Drive (6dB warmth)")          # 0-24

# Filter Envelope — opens up slowly (part of the "evolving")
set_param(176, 55.0, "Fe Amount (+55 = opens up)")         # -100 to 100
set_param(178, 0.30, "Fe Attack (~25ms)")
set_param(181, 0.75, "Fe Decay (~1s slow evolve)")         # slow = evolving feel
set_param(184, 0.30, "Fe Sustain (30% open)")
set_param(185, 0.65, "Fe Release")

print()

# ── SHAPER — adds metallic edge/grit ────────────────────────
# Shaper Mix: 0-100, Drive: -12 to 12
set_param(192, 2.0,  "Shaper Type (Soft Clip)")            # 0-4, 2=soft saturation
set_param(193, 35.0, "Shaper Mix (35% wet)")               # 0-100
set_param(194, 4.0,  "Shaper Drive (+4dB)")                # -12 to 12

# ── GLOBAL ───────────────────────────────────────────────────
set_param(4,  0.82, "Volume (0.82)")
set_param(8,  0.65, "Tone (slightly bright)")
set_param(9,  0.15, "Spread (subtle stereo width)")

print()
print("=" * 60)
print("  VERIFYING KEY PARAMETERS...")
print("=" * 60)

checks = [
    (1,   "Algorithm"),
    (40,  "B Coarse (expect 7)"),
    (67,  "C Coarse (expect 11)"),
    (47,  "Osc-B Level"),
    (122, "Pe On"),
    (124, "Pe Init (expect 12st)"),
    (141, "LFO On"),
    (144, "LFO Rate"),
    (170, "Filter Freq"),
    (176, "Fe Amount"),
    (193, "Shaper Mix"),
]
for idx, name in checks:
    v = read_param(idx)
    print(f"  [{idx:3d}] {name:<30} = {v}")

print()
print("✅ METALLIC EVOLVING LEAD PATCH COMPLETE!")
print("   Play long notes to hear the filter evolve.")
print("   Short staccato notes = metallic zing from pitch env.")

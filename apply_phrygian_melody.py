import socket, json, time

TRACK = 1
CLIP_SLOT = 0

def send(address, args=[]):
    msg = json.dumps({'jsonrpc': '2.0', 'id': 'melody', 'method': 'send_message',
                      'params': {'address': address, 'args': args}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(6)
    s.connect(('127.0.0.1', 65432))
    s.sendall(msg.encode())
    time.sleep(0.5)
    try:
        data = s.recv(131072)
        s.close()
        return json.loads(data.decode())
    except Exception as e:
        s.close()
        return {'error': str(e)}

print("=" * 62)
print("  PHRYGIAN D MELODY REWRITE (AFX / Atonal Style)")
print("  Mode: D Phrygian (D Eb F G A Bb C D)")
print("  Length: 8 bars, long irregular notes")
print("=" * 62)
print()

# -- D PHRYGIAN MIDI NOTES --
# D2=38, Eb2=39, F2=41, G2=43, A2=45, Bb2=46, C3=48
# D3=50, Eb3=51, F3=53, G3=55, A3=57, Bb3=58, C4=60, D4=62
# Eb4=63, F4=65

# AFX-style: Irregular durations, lots of rests, quarter tones implied
# by the FM microtonal detuning. Notes held long = evolving timbre.
#
# 8 bars = 32 beats at any BPM
# Format per note: [pitch, time, duration, velocity, mute=0]
#
# D Phrygian phrase with characteristic b2 (Eb) and dark b6 (Bb)
# AFX influence: unexpected rhythmic placement, long sustains, sudden jumps

notes = [
    # Bar 1-2: Open with long D root, then the characteristic Eb (b2)
    # [pitch, beat_start, duration, velocity, mute]
    [50, 0.0,   3.0,  90, 0],   # D3  - long opening root
    [51, 3.0,   0.75, 75, 0],   # Eb3 - b2, characteristic Phrygian note
    [50, 3.75,  0.5,  65, 0],   # D3  - quick return
    [48, 4.5,   1.75, 80, 0],   # C3  - b7, creates AFX-style downward tension
    # Bar 3: Descend through dark notes
    [46, 6.5,   2.5,  85, 0],   # Bb2 - b6, very dark
    [45, 9.0,   0.75, 70, 0],   # A2  - p5
    # Bar 4: Low G held long (modal anchor)
    [43, 9.75,  3.5,  88, 0],   # G2  - p4, long held

    # Bar 5: Ascent starts - Phrygian climb
    [46, 13.5,  1.0,  72, 0],   # Bb2 - b6
    [48, 14.5,  0.5,  68, 0],   # C3  - b7
    [50, 15.0,  0.75, 78, 0],   # D3  - root restatement
    [51, 15.75, 1.5,  82, 0],   # Eb3 - b2 held longer this time

    # Bar 6: High register - AFX sudden octave jump
    [60, 17.5,  0.5,  95, 0],   # C4  - high b7, accent
    [58, 18.0,  2.0,  80, 0],   # Bb3 - b6 up octave, long
    [55, 20.0,  1.5,  75, 0],   # G3  - p4

    # Bar 7: Dissonant AFX-style cluster movement
    [53, 21.5,  0.5,  88, 0],   # F3  - p3 (minor 3rd)
    [51, 22.0,  0.75, 92, 0],   # Eb3 - b2 (tension!)
    [53, 22.75, 0.5,  70, 0],   # F3  - back up
    [55, 23.25, 0.75, 65, 0],   # G3  - resolution attempt

    # Bar 8: Final resolution - long D root, Phrygian cadence
    [48, 24.0,  1.5,  78, 0],   # C3  - approach from b7
    [50, 25.5,  0.75, 85, 0],   # D3  - root
    [51, 26.25, 0.5,  72, 0],   # Eb3 - b2 (Phrygian signature)
    [50, 26.75, 5.25, 88, 0],   # D3  - final long root (bleeds past loop for reverb)
]

# Step 1: Check clip exists
print("Checking current clip on Track 1, Slot 0...")
r = send('/live/clip/get/length', [TRACK, CLIP_SLOT])
print(f"  Current length: {r}")

# Step 2: Delete all existing notes
print("Deleting existing notes...")
r = send('/live/clip/remove/notes', [TRACK, CLIP_SLOT, 0, 0, 128, 32])
print(f"  Remove result: {r.get('result', {}).get('status')}")

# Step 3: Set clip to 8 bars (32 beats)
print("Setting clip length to 8 bars (32 beats)...")
r = send('/live/clip/set/loop_end', [TRACK, CLIP_SLOT, 32.0])
print(f"  Loop end: {r.get('result', {}).get('status')}")

# Step 4: Add all Phrygian D notes
print(f"Adding {len(notes)} notes in D Phrygian...")
flat_notes = []
for n in notes:
    flat_notes.extend(n)

args = [TRACK, CLIP_SLOT] + flat_notes
r = send('/live/clip/add/notes', args)
print(f"  Add notes result: {r.get('result', {}).get('status')}")

print()
print("=" * 62)
print("  D PHRYGIAN NOTE MAP:")
print("  D=50  Eb=51  F=53  G=55  A=57  Bb=58  C=60  D4=62")
print()
print("  Bar 1-2: D3 (long) -> Eb3 (b2) -> D3 -> C3 (b7)")
print("  Bar 3-4: Bb2 (b6) -> A2 -> G2 (long anchor)")
print("  Bar 5:   Bb2 -> C3 -> D3 -> Eb3 (b2 held)")
print("  Bar 6:   C4 (high accent!) -> Bb3 -> G3")
print("  Bar 7:   F3 -> Eb3(!) -> F3 -> G3 (AFX cluster)")
print("  Bar 8:   C3 -> D3 -> Eb3 -> D3 (long resolve)")
print()
print("MELODY REWRITE COMPLETE")
print("Set clip to loop and play - notes evolve with the FM timbre!")

# Ableton Operator — OSC/MCP Programming Guide

> **Purpose**: This file is a permanent memory and reference for programming Ableton's Operator synthesizer
> via the AbletonOSC MCP server. Read this before writing any Operator patch script.

---

## 🔑 Critical Rules (Learned the Hard Way)

### 1. ALL parameters use their NATIVE unit ranges — NOT always 0–1
- Most amplitude/time envelopes: **0.0 – 1.0** (internally mapped to ms by Ableton)
- Some params like `Algorithm`, `Coarse`, `Filter Drive`, `Fe Amount` use **their actual unit values**
- **ALWAYS query min/max before setting** — never assume 0–1

### 2. The set endpoint is fire-and-forget — always verify
- `/live/device/set/parameter/value` returns `{"status": "sent"}` — this does NOT confirm Ableton applied the change
- **Always read back** with `/live/device/get/parameter/value` to verify
- Use `/live/device/get/parameters/value` (plural) to dump all at once for verification

### 3. The OSC daemon returns "sent" even if the value is out of range
- Out-of-range values are silently clamped or ignored by Ableton Live
- Example: sending `3500.0` for `Filter Freq` (range 0–1) results in it being set to `1.0` (max)

---

## 📡 OSC Endpoints Reference

### Read All Parameters At Once (FAST — use these)
```
/live/device/get/parameters/name      [track_idx, device_idx]  → all names
/live/device/get/parameters/value     [track_idx, device_idx]  → all current values
/live/device/get/parameters/min       [track_idx, device_idx]  → all min values
/live/device/get/parameters/max       [track_idx, device_idx]  → all max values
/live/device/get/parameters/is_quantized  [track_idx, device_idx]  → booleans
```

### Read/Set Individual Parameters
```
/live/device/get/parameter/value      [track, device, param_idx]        → value
/live/device/get/parameter/name       [track, device, param_idx]        → name
/live/device/set/parameter/value      [track, device, param_idx, value] → "sent"
/live/device/get/parameter/value_string [track, device, param_idx]      → "2500 Hz" style
```

### Device Info
```
/live/track/get/num_devices           [track_idx]              → count
/live/device/get/name                 [track, device]          → "Operator"
/live/device/get/num_parameters       [track, device]          → 195 for Operator
```

> **Note**: There is NO `/live/device/get/parameter/min` (singular). Only `/live/device/get/parameters/min` (plural) exists.

---

## 🗺️ Operator Parameter Index Map

Operator on a standard patch has **195 parameters** (index 0–194).

### Global
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 0 | Device On | 0–1 | 1 = on |
| 1 | Algorithm | 0–10 | 11 FM routing algorithms |
| 2 | Transpose | -24–24 | semitones |
| 3 | PB Range | 0–24 | pitch bend range |
| 4 | Volume | 0–1 | normalized |
| 5 | Panorama | 0–1 | 0.5 = center |
| 8 | Tone | 0–1 | brightness |
| 9 | Spread | 0–1 | stereo spread (Unison) |
| 10 | Glide On | 0–1 | portamento on/off |
| 11 | Glide Time | 0–1 | portamento time |

### Oscillator A (Carrier or Modulator depending on Algorithm)
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 12 | Osc-A On | 0–1 | 1 = active |
| 13 | A Coarse | 0–48 | ratio multiplier (integer steps) |
| 14 | A Fine | **0–1000** | fine detune in cents×10. **500 = 0 cents (center)**. 570=+7ct, 650=+15ct (near quarter-tone), 340=-16ct |
| 16 | A Quantize | 0–1 | quantize ratio |
| 17 | A Fix On | 0–1 | fixed frequency mode |
| 18 | A Fix Freq | 0–1 | fixed freq (normalized) |
| 20 | Osc-A Level | 0–1 | output level |
| 22 | Osc-A Phase | 0–1 | starting phase |
| 25 | Osc-A Wave | 0–22 | waveform (0=Sine, 1=Saw…) |
| 26 | Osc-A Feedb | 0–100 | self-feedback amount (NOT 0-1!) |
| 29 | Ae Attack | 0–1 | amp envelope attack |
| 31 | Ae Decay | 0–1 | amp envelope decay |
| 33 | Ae Sustain | 0–1 | amp envelope sustain |
| 34 | Ae Release | 0–1 | amp envelope release |

### Oscillator B
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 39 | Osc-B On | 0–1 | |
| 40 | B Coarse | 0–48 | ratio multiplier |
| 41 | B Fine | **0–1000** | 500=0ct center. 420=-8ct, 580=+8ct |
| 47 | Osc-B Level | 0–1 | mod depth when used as modulator |
| 52 | Osc-B Wave | 0–22 | |
| 53 | Osc-B Feedb | 0–100 | self-feedback (NOT 0-1!) |
| 56 | Be Attack | 0–1 | |
| 58 | Be Decay | 0–1 | |
| 60 | Be Sustain | 0–1 | |
| 61 | Be Release | 0–1 | |

### Oscillator C
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 66 | Osc-C On | 0–1 | |
| 67 | C Coarse | 0–48 | |
| 74 | Osc-C Level | 0–1 | |
| 79 | Osc-C Wave | 0–22 | |
| 80 | Osc-C Feedb | 0–100 | |
| 83 | Ce Attack | 0–1 | |
| 85 | Ce Decay | 0–1 | |
| 87 | Ce Sustain | 0–1 | |
| 88 | Ce Release | 0–1 | |

### Oscillator D
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 93 | Osc-D On | 0–1 | |
| 94 | D Coarse | 0–48 | |
| 101 | Osc-D Level | 0–1 | |
| 106 | Osc-D Wave | 0–22 | |
| 107 | Osc-D Feedb | 0–100 | |
| 110 | De Attack | 0–1 | |
| 112 | De Decay | 0–1 | |
| 114 | De Sustain | 0–1 | |
| 115 | De Release | 0–1 | |

### Pitch Envelope
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 122 | Pe On | 0–1 | enable pitch envelope |
| 123 | Pe Attack | 0–1 | normalized time |
| 124 | Pe Init | -48–48 | initial pitch offset in semitones |
| 125 | Pe A Slope | -1–1 | attack curve shape |
| 126 | Pe Decay | 0–1 | normalized time |
| 127 | Pe Peak | -48–48 | peak pitch in semitones |
| 128 | Pe D Slope | -1–1 | decay curve shape |
| 129 | Pe Sustain | -48–48 | sustain pitch in semitones |
| 130 | Pe Release | 0–1 | normalized time |
| 131 | Pe End | -48–48 | end pitch in semitones |
| 132 | Pe R Slope | -1–1 | release curve shape |
| 133 | Pe Mode | 0–4 | envelope mode |
| 137 | Pe Amount | -1–1 | **NORMALIZED** (-1 to 1, maps to full pitch range) |
| 138 | Pe Amt A | -100–100 | amount sent to Osc A |
| 139 | Pe Dst B | 0–23 | secondary destination selector |
| 140 | Pe Amt B | -100–100 | amount to destination B |

### LFO
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 141 | LFO On | 0–1 | |
| 142 | LFO Type | 0–6 | 0=Sine, 1=Square, 2=Tri, 3=SawUp, 4=SawDown, 5=S&H, 6=? |
| 143 | LFO Range | 0–2 | 0=Low, 1=Mid, 2=Hi |
| 144 | LFO Rate | **0–127** | NOT 0-1! Use 0-127 range |
| 145 | LFO Sync | 0–14 | sync division steps (0=free) |
| 146 | LFO R < K | 0–1 | rate < key tracking |
| 147 | LFO Retrigger | 0–1 | retrigger on note on |
| 148 | LFO Amt | **0–1** | amount to primary destination |
| 149 | LFO Amt A | -100–100 | amount to Osc A |
| 150 | LFO Dst B | 0–23 | secondary destination selector |
| 151 | LFO Amt B | -100–100 | amount to destination B |
| 152 | LFO < Vel | -1–1 | velocity → LFO amount modulation |
| 153 | LFO < Pe | 0–1 | pitch env → LFO amount |

### Filter
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 165 | Filter On | 0–1 | |
| 166 | Filter Type | 0–4 | 0=LP, 1=HP, 2=BP, 3=Notch, 4=Morph |
| 170 | Filter Freq | 0–1 | **NORMALIZED** (not Hz!) |
| 171 | Filter Res | 0–1.25 | resonance |
| 173 | Filter Drive | 0–24 | saturation in dB |
| 176 | Fe Amount | -100–100 | filter envelope amount |
| 178 | Fe Attack | 0–1 | |
| 181 | Fe Decay | 0–1 | |
| 184 | Fe Sustain | 0–1 | |
| 185 | Fe Release | 0–1 | |

### Shaper
| Idx | Name | Range | Notes |
|-----|------|-------|-------|
| 192 | Shaper Type | 0–4 | waveshaper algorithm |
| 193 | Shaper Mix | **0–100** | dry/wet (NOT 0-1!) |
| 194 | Shaper Drive | **-12–12** | drive in dB |

---

## 📐 Envelope Time Approximations (0–1 normalized → ms)

These are **approximate** mappings — Ableton uses a non-linear curve:

| Value | Approx Time |
|-------|-------------|
| 0.00 | ~0 ms (instant) |
| 0.05 | ~2 ms |
| 0.10 | ~8 ms |
| 0.20 | ~25 ms |
| 0.35 | ~60 ms |
| 0.42 | ~90 ms |
| 0.48 | ~130 ms |
| 0.55 | ~200 ms |
| 0.63 | ~350 ms |
| 0.70 | ~600 ms |
| 0.80 | ~1.5 s |
| 0.90 | ~4 s |
| 1.00 | ~60 s |

---

## 🎛️ Algorithm Routing Reference (Operator)

Operator has **11 algorithms (0–10)**. The exact routings:

| Idx | Routing Description |
|-----|---------------------|
| 0 | A, B, C, D — all parallel carriers (additive) |
| 1 | B→A carrier; C, D carriers |
| 2 | C→B→A; D carrier |
| 3 | B→A, D→C (two independent pairs) |
| 4 | B→A, C→A; D carrier (two mods → one carrier) |
| 5 | D→C→B→A (full 4-op linear chain) |
| 6 | C→B→A, D→A (three mods → A carrier) |
| 7 | B→A, C→A, D→A (three mods → one carrier) |
| 8 | D→C, B→A, both carriers |
| 9 | D→C→A, B→A (two stacks merged) |
| 10 | D→A, C→A, B→A, all mods to A |

> **For metallic sounds**: Use algorithms 4, 6, 7 (multiple mods into one carrier = complex inharmonics)
> **For bass**: Use algorithm 1 or 3 (single modulator for controlled FM)
> **For additive/complex**: Use algorithm 0 with detuned carriers

---

## 🔊 Waveform Index Reference (Wave param: 0–22)

| Idx | Waveform |
|-----|----------|
| 0 | Sine |
| 1 | Downsaw |
| 2 | Upsaw |
| 3 | Square |
| 4 | Triangle |
| 5–22 | Harmonic/Partials variations |

---

## 🎨 Preset Patch Recipes

### Classic FM Bass (electro/dance)
```
Algorithm: 1 (B→A)
A: Sine, Coarse=1, Level=1.0
B: Sine, Coarse=2, Level=0.65
Ae: Attack=0.0, Decay=0.55, Sus=0, Rel=0.45
Be: Attack=0.0, Decay=0.42, Sus=0, Rel=0.35
Filter: LP, Freq=0.68, Res=0.18, Drive=8.0
Fe Amount=40, Fe Decay=0.48
```

### Metallic Evolving Lead
```
Algorithm: 4 (B,C→A; D carrier)
A: Sine, Coarse=1
B: Sine, Coarse=7, Level=0.7  ← inharmonic = metallic
C: Sine, Coarse=11, Level=0.4 ← higher inharmonic partial
D: Sine, Coarse=1, Level=0.3  ← sub carrier for body
Feedback on B: ~0.3
Pitch Env On, Amount=12st, fast attack, medium decay
LFO: Sine, slow rate, modulating Filter Freq (~0.15 amt)
Filter: LP, Freq=0.60, Res=0.35, Drive=6
Ae: Attack=0.02, Decay=0.75, Sus=0.4, Rel=0.65
```

---

## 🐛 Known Bugs / Gotchas

1. **`get/parameter/min` (singular) does NOT exist** — use `get/parameters/min` (plural)
2. **`set` commands return `"sent"` not `"success"`** — this is normal, not an error
3. **Sending values > max**: Ableton clamps silently, NO error returned
4. **Track index**: Always 0-based. Track 0 = first track visible in session
5. **Device index**: 0-based. If only one device on track, device_index=0
6. **Response timeout**: If Ableton is minimized or frozen, OSC responses time out after ~5s
7. **Parameter 120 (Time)**: Global LFO speed multiplier — changing this affects all LFO rates

---

## ✅ Workflow for Programming a New Patch

```python
# Step 1: Verify track and device
r = send('/live/track/get/name', [track_idx])
r = send('/live/device/get/name', [track_idx, device_idx])

# Step 2: Get ALL min/max ranges FIRST
mins = send('/live/device/get/parameters/min', [track_idx, device_idx])
maxs = send('/live/device/get/parameters/max', [track_idx, device_idx])
names = send('/live/device/get/parameters/name', [track_idx, device_idx])

# Step 3: Set parameters with CORRECT normalized values
send('/live/device/set/parameter/value', [track, device, param_idx, correct_value])

# Step 4: ALWAYS verify after setting
vals = send('/live/device/get/parameters/value', [track_idx, device_idx])
# Check target params have the expected values
```

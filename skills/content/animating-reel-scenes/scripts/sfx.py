"""Write one sound-effects track for the whole reel, synthesised here so there is no third-party sample to license.

  python3 sfx.py exports/00-sfx.wav --duration 80.9 --scene cenas/01-name.html 9.96 --scene cenas/04-name.html 55.9
  python3 sfx.py exports/00-sfx.wav --duration 80.9 --events cenas/sfx.json

Each scene lists its own sounds next to its timing table, in seconds from the scene start:
  window.SFX = [{"t": 0.68, "kind": "pop"}, {"t": 5.02, "kind": "draw"}];
and --scene FILE START shifts them onto the reel's clock. --events takes the same list already on the reel's
clock. The file goes on an audio track at 00:00:00:00 in CapCut. Kinds:
  pop      a soft thump: a sticker, note or node stamps in
  thud     a deeper, heavier pop: a state change that matters (a node turns red, a block is replaced)
  tick     a dry click: a small label, a typed word, a step in a sequence
  draw     a short pen scratch: a line or connector is traced
  whoosh   a rising sweep: a scene or panel comes in
  out      a falling sweep: a scene, panel or overlay goes away
  ding     a light bell: a check, a loop that closes, a right answer
Optional "gain" per event (default 1.0). Levels sit well under speech; the author sets the final volume in CapCut.
"""
import argparse, json, math, random, re, struct, sys, wave

SR = 48000  # CapCut project audio rate

def env(i, n, attack=.004):
    return min(1, (i / SR) / attack) * math.exp(-6 * i / n)

def sweep_down(f0, f1, dur, amp):
    n, out, ph = int(dur * SR), [], 0.0
    for i in range(n):
        ph += 2 * math.pi * (f0 + (f1 - f0) * i / n) / SR  # falling pitch reads as something landing
        out.append(amp * env(i, n) * math.sin(ph))
    return out

def noise_sweep(dur, rising, seed, amp=.5):
    r, y, out, n = random.Random(seed), 0.0, [], int(dur * SR)
    for i in range(n):
        k = i / n if rising else 1 - i / n
        y += (.02 + .25 * k) * ((r.random() * 2 - 1) - y)  # low-pass that opens (or closes) over the sweep
        out.append(amp * math.sin(math.pi * i / n) * y)
    return out

def tick(n=int(.012 * SR)):
    r = random.Random(1)
    return [.35 * math.exp(-8 * i / n) * (r.random() * 2 - 1) for i in range(n)]

def draw(dur=.26):
    r, n, prev, out = random.Random(3), int(dur * SR), 0.0, []
    for i in range(n):
        x = r.random() * 2 - 1
        hp = x - prev; prev = x  # high-passed noise: the grain of a pen on paper
        trem = .6 + .4 * math.sin(2 * math.pi * 38 * i / SR)
        out.append(.22 * math.sin(math.pi * i / n) * trem * hp)
    return out

def ding(n=int(.5 * SR)):
    return [.25 * math.exp(-5 * i / n) * (math.sin(2 * math.pi * 1320 * i / SR) + .4 * math.sin(2 * math.pi * 2640 * i / SR)) for i in range(n)]

KINDS = {'pop': sweep_down(170, 70, .12, .55), 'thud': sweep_down(110, 42, .22, .75), 'tick': tick(), 'draw': draw(),
         'whoosh': noise_sweep(.32, True, 2), 'out': noise_sweep(.28, False, 4, .42), 'ding': ding()}

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--duration', type=float, required=True)
ap.add_argument('--events'); ap.add_argument('--scene', nargs=2, action='append', metavar=('FILE', 'START'), default=[])
a = ap.parse_args()
events = json.load(open(a.events)) if a.events else []
for f, start in a.scene:
    m = re.search(r'window\.SFX\s*=\s*(\[.*?\]);', open(f, encoding='utf-8').read(), re.S)
    if not m: sys.exit(f'{f}: no window.SFX = [...]; list the scene sounds next to its timing table')
    events += [dict(e, t=round(e['t'] + float(start), 3)) for e in json.loads(m.group(1))]
buf = [0.0] * int(a.duration * SR)
for e in events:
    if e['kind'] not in KINDS: sys.exit(f"unknown kind {e['kind']!r}; use one of {', '.join(KINDS)}")
    s0, g = int(e['t'] * SR), e.get('gain', 1.0)
    for i, v in enumerate(KINDS[e['kind']]):
        if 0 <= s0 + i < len(buf): buf[s0 + i] += g * v
peak = max(1e-9, max(abs(v) for v in buf))
scale = .3 / peak  # peak near -10 dBFS: under a voice recorded near -3 dB, and never clipping where events overlap
with wave.open(a.out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(32767 * scale * v)) for v in buf))
print(a.out, len(events), 'events', f'{a.duration:.2f}s')

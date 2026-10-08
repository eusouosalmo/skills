"""Write one sound-effects track for the whole reel, synthesised here so there is no third-party sample to license.

  python3 sfx.py events.json exports/NN-sfx.wav --duration 80.7

events.json: [{"t": 11.81, "kind": "pop"}, {"t": 16.43, "kind": "tick"}, ...], t in seconds on the reel's clock,
so the file goes on an audio track at 00:00:00:00 in CapCut. Kinds:
  pop    a soft low thump for a sticker stamp
  tick   a dry click for a highlight or a typed word
  whoosh a short airy sweep for a cut to a full-screen scene
  ding   a light bell for a check or a correct answer
Optional "gain" per event (default 1.0). Levels sit well under speech; the author sets the final volume in CapCut.
"""
import argparse, json, math, random, struct, sys, wave

SR = 48000  # CapCut project audio rate

def env(i, n, attack=.004):
    t = i / SR
    return min(1, t / attack) * math.exp(-6 * i / n)

def pop(n=int(.12 * SR)):
    out, ph = [], 0.0
    for i in range(n):
        f = 170 - 100 * i / n  # pitch falls from 170 to 70 Hz: reads as a soft landing
        ph += 2 * math.pi * f / SR
        out.append(.55 * env(i, n) * math.sin(ph))
    return out

def tick(n=int(.012 * SR)):
    r = random.Random(1)
    return [.35 * math.exp(-8 * i / n) * (r.random() * 2 - 1) for i in range(n)]

def whoosh(n=int(.32 * SR)):
    r, y, out = random.Random(2), 0.0, []
    for i in range(n):
        k = i / n
        a = .02 + .25 * k  # low-pass opens as it goes: a rising sweep
        y += a * ((r.random() * 2 - 1) - y)
        out.append(.5 * math.sin(math.pi * k) * y)
    return out

def ding(n=int(.5 * SR)):
    return [.25 * math.exp(-5 * i / n) * (math.sin(2 * math.pi * 1320 * i / SR) + .4 * math.sin(2 * math.pi * 2640 * i / SR)) for i in range(n)]

KINDS = {'pop': pop(), 'tick': tick(), 'whoosh': whoosh(), 'ding': ding()}

ap = argparse.ArgumentParser()
ap.add_argument('events'); ap.add_argument('out'); ap.add_argument('--duration', type=float, required=True)
a = ap.parse_args()
events = json.load(open(a.events))
buf = [0.0] * int(a.duration * SR)
for e in events:
    if e['kind'] not in KINDS: sys.exit(f"unknown kind {e['kind']!r}; use one of {', '.join(KINDS)}")
    s0, g = int(e['t'] * SR), e.get('gain', 1.0)
    for i, v in enumerate(KINDS[e['kind']]):
        if s0 + i < len(buf): buf[s0 + i] += g * v
peak = max(1e-9, max(abs(v) for v in buf))
scale = min(1.0, .7 / peak)  # never clip, even when events overlap
with wave.open(a.out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(32767 * scale * v)) for v in buf))
print(a.out, len(events), 'events', f'{a.duration:.2f}s')

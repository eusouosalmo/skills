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
  drip     a water drop: a drop falls, a liquid drips
  splash   liquid landing: a drop or a pour hits liquid
  swirl    stirring: a liquid mixes, something churns
  coin     a metal clink: a coin, a token, a key put down
  slide    a soft brush: an object travels or slides across the stage
  lock     a mechanical click: a lock, a latch, a switch
  snap     a sharp finger snap: the single key point, used rarely
  warble   a wobbling tone: a shape morphs into another
  boing    a spring: something lands and bounces into place
  stamp    a rubber stamp: a seal or stamped label lands
  paper    a page slides or flips: a card, a page, a note moves
  sparkle  rising pings: a reveal, the answer appears
  chime    a two-note ta-da: something works, a right result
  buzz     a low buzz: an error, a failed attempt, a blocked path
  notify   two soft blips: a message or notification arrives
  typing   a run of keystrokes: code or text being typed
  gear     a ratchet: a mechanism advances step by step
  glass    glass breaking: something cracks or shatters
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

# Material sounds: when the object on screen is made of something, the ear expects that thing.
def drip(dur=.09):
    n, out, ph = int(dur * SR), [], 0.0
    for i in range(n):
        ph += 2 * math.pi * (380 + 1100 * (i / n) ** .5) / SR  # rising pitch: the "bloop" of a drop
        out.append(.5 * math.exp(-5 * i / n) * math.sin(ph))
    return out

def splash(dur=.3):
    r, y, n = random.Random(5), 0.0, int(dur * SR)
    noise = []
    for i in range(n):
        y += .35 * ((r.random() * 2 - 1) - y)  # bright noise burst that settles: liquid landing
        noise.append(.5 * math.exp(-9 * i / n) * y)
    return [a + b for a, b in zip(noise, sweep_down(160, 60, dur, .35) + [0] * n)]

def swirl(dur=.75):
    r, y, n, out = random.Random(6), 0.0, int(dur * SR), []
    for i in range(n):
        y += .06 * ((r.random() * 2 - 1) - y)
        wob = .55 + .45 * math.sin(2 * math.pi * 7 * i / SR)  # turns of the stir
        out.append(.9 * math.sin(math.pi * i / n) * wob * y)
    return out

def coin(dur=.45):
    n = int(dur * SR)
    parts = [(2210, 1), (3470, .6), (5130, .35)]  # inharmonic partials: metal
    return [.22 * math.exp(-7 * i / n) * sum(a * math.sin(2 * math.pi * f * i / SR) for f, a in parts) for i in range(n)]

def slide(dur=.42):
    return noise_sweep(dur, True, 7, .5)  # a soft, low brush: something moving across the stage

def lock():
    t = tick(); gap = [0.0] * int(.06 * SR)
    return [a + b for a, b in zip(t + gap + t + [0.0] * int(.2 * SR), [0.0] * (len(t) + len(gap)) + sweep_down(140, 60, .2, .4) + [0.0] * len(t))]

# Event sounds after the groups explainer packs use (clicks, springs, paper, reveals, mechanical, UI); see sources.md.
def mix(*parts):  # (offset in s, samples) pairs summed into one sound
    n = max(int(o * SR) + len(x) for o, x in parts); out = [0.0] * n
    for o, x in parts:
        for i, v in enumerate(x): out[int(o * SR) + i] += v
    return out

def tone(partials, dur, decay, amp, f_end=None):
    n, out = int(dur * SR), []
    for i in range(n):
        k = 1 if f_end is None else (f_end / partials[0][0]) ** (i / n)
        out.append(amp * math.exp(-decay * i / n) * sum(a * math.sin(2 * math.pi * f * k * i / SR) for f, a in partials))
    return out

def burst(dur, cutoff, seed, amp, decay=10):
    r, y, n, out = random.Random(seed), 0.0, int(dur * SR), []
    for i in range(n):
        y += cutoff * ((r.random() * 2 - 1) - y)
        out.append(amp * math.exp(-decay * i / n) * y)
    return out

def snap():      # a sharp finger snap: emphasis on one key point, used rarely
    return mix((0, burst(.05, .9, 8, .55, 14)), (0, tone([(2800, 1)], .04, 12, .15)))

def warble(dur=.34):  # a shape morphing: pitch wobbles while it changes
    n, out, ph = int(dur * SR), [], 0.0
    for i in range(n):
        ph += 2 * math.pi * (420 + 90 * math.sin(2 * math.pi * 14 * i / SR)) / SR
        out.append(.5 * math.sin(math.pi * i / n) * math.sin(ph))
    return out

def boing(dur=.45):   # a spring: something lands and bounces into place
    n, out, ph = int(dur * SR), [], 0.0
    for i in range(n):
        ph += 2 * math.pi * (180 + 160 * math.exp(-5 * i / n) * (1 + .5 * math.sin(2 * math.pi * 22 * i / SR))) / SR
        out.append(.45 * math.exp(-4 * i / n) * math.sin(ph))
    return out

def stamp():     # a rubber stamp: a dull thump with the slap of paper
    return mix((0, sweep_down(130, 55, .16, .7)), (0, burst(.07, .5, 9, .45, 12)))

def paper(dur=.22):   # a page slides or flips: bright, airy noise
    r, prev, n, out = random.Random(10), 0.0, int(dur * SR), []
    for i in range(n):
        x = r.random() * 2 - 1; hp = x - prev; prev = x
        out.append(.35 * math.sin(math.pi * i / n) ** 2 * hp)
    return out

def sparkle():   # a reveal: a short run of high, rising pings
    r = random.Random(11)
    return mix(*[(j * .045, tone([(2000 + j * 260 + r.random() * 150, 1), (5200 + j * 300, .3)], .18, 8, .32)) for j in range(7)])

def chime():     # a positive two-note "ta-da": something works, a result that is right
    return mix((0, tone([(784, 1), (1568, .3)], .3, 5, .4)), (.12, tone([(1175, 1), (2350, .3)], .5, 4, .4)))

def buzz(dur=.28):    # a negative cue: an error, a failed attempt, a blocked path
    n = int(dur * SR)
    return [.45 * math.exp(-2 * i / n) * (1 if math.sin(2 * math.pi * 110 * i / SR) > 0 else -1) * min(1, i / 200) for i in range(n)]

def notify():    # a message arrives: two quick soft blips (generic, not any app's sound)
    return mix((0, tone([(880, 1)], .09, 6, .45)), (.11, tone([(1320, 1)], .14, 5, .45)))

def typing(keys=6, gap=.065):  # keys on a keyboard: code or text being typed
    r = random.Random(12)
    return mix(*[(j * gap + r.random() * .015, mix((0, burst(.02, .7, 20 + j, .5, 12)), (0, tone([(1900 + r.random() * 600, 1)], .015, 10, .08)))) for j in range(keys)])

def gear():      # a ratchet turning: a mechanism advances step by step
    return mix(*[(j * .05, burst(.018, .8, 30 + j, .45, 14)) for j in range(4)])

def glass():     # glass cracks and breaks: a burst with scattered metallic shards
    r = random.Random(13)
    shards = [(r.random() * .25, tone([(3000 + r.random() * 4000, 1)], .12, 9, .1)) for _ in range(9)]
    return mix((0, burst(.3, .6, 14, .55, 7)), *shards)

KINDS = {'pop': sweep_down(170, 70, .12, .55), 'thud': sweep_down(110, 42, .22, .75), 'tick': tick(), 'draw': draw(),
         'whoosh': noise_sweep(.32, True, 2), 'out': noise_sweep(.28, False, 4, .42), 'ding': ding(),
         'drip': drip(), 'splash': splash(), 'swirl': swirl(), 'coin': coin(), 'slide': slide(), 'lock': lock(),
         'snap': snap(), 'warble': warble(), 'boing': boing(), 'stamp': stamp(), 'paper': paper(), 'sparkle': sparkle(),
         'chime': chime(), 'buzz': buzz(), 'notify': notify(), 'typing': typing(), 'gear': gear(), 'glass': glass()}

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

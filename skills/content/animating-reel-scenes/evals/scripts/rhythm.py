"""Count visual events in a rendered scene, the caption band masked out.

Usage: python3 rhythm.py video.mp4 [caption_top caption_bottom] [--panel]
Caption band as fractions of the height (default 0.68 0.80). With --panel, only the
top 1080x960 half is measured (a split-screen panel) and no band is masked. Prints events per 10 s
and the longest stretch with no new state, in seconds.
"""
import sys, subprocess, numpy as np
STEP, PIX, EVENT, HOLD, BURST, BURST_MAX = 4, 0.10, 0.02, 2, 1.0, 3.0
args = [a for a in sys.argv[1:] if a != '--panel']
panel = '--panel' in sys.argv
video = args[0]
lo, hi = (float(args[1]), float(args[2])) if len(args) > 2 else (0.68, 0.80)
if panel: lo = hi = 1.0
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'fps={STEP},' + ('crop=iw:ih/2:0:0,' if panel else '') + 'scale=108:192,format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(np.float32) / 255
mask = np.ones((192, 108), bool); mask[int(lo * 192):int(hi * 192), :] = False
dur = len(fr) / STEP
kept, keep = fr[0], []
for i in range(1, len(fr) - HOLD):
    moved = np.abs(fr[i] - kept) > PIX; holds = np.abs(fr[i] - fr[i + HOLD]) < PIX
    if (moved & holds & mask).sum() / mask.size > EVENT:
        kept = fr[i]; keep.append(i)
ev = []
for k in keep:
    t = k / STEP
    if ev and t - ev[-1][1] < BURST and t - ev[-1][0] < BURST_MAX: ev[-1][1] = t
    else: ev.append([t, t])
s = [0.0] + [e[0] for e in ev] + [dur]
gaps = [b - a for a, b in zip(s, s[1:])]
print(f"events_per_10s={len(ev) / dur * 10:.2f} longest_still_s={max(gaps):.2f} events_at={[round(e[0], 2) for e in ev]}")

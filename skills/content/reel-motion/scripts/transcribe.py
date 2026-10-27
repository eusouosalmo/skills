"""Time every spoken word of a recording with Whisper, keeping the author's SRT text when there is one.

  python transcribe.py recording.mp4 --srt narration.srt -o words.json
  python transcribe.py recording.mp4 -o words.json          # no SRT: Whisper's own text

Output: words.json, a list of {"w": word, "s": start, "e": end, "cue": SRT index or null, "src": "whisper" | "interp"},
and the same table printed as `start  end  word` for reading. Times are seconds on the recording's clock,
which is the CapCut timeline when the recording starts at 0.

Whisper misreads names ("Claude" as "Cloud"), so with --srt the words and their order come from the SRT and
only the times come from Whisper. Words Whisper missed get times interpolated inside their cue (src "interp").
Run with the python that setup.sh reports for faster-whisper.
"""
import argparse, difflib, json, re, shutil, subprocess, sys, unicodedata

try:
    import numpy as np
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit('faster-whisper missing: run bash scripts/setup.sh')
if not shutil.which('ffmpeg'):
    sys.exit('ffmpeg not found on PATH: run bash scripts/setup.sh')

ap = argparse.ArgumentParser()
ap.add_argument('media')
ap.add_argument('--srt')
ap.add_argument('-o', '--out', default='words.json')
ap.add_argument('--model', default='small')  # small: about 20 s per minute on CPU; large-v3 is slower and more accurate
ap.add_argument('--lang', default='pt')
a = ap.parse_args()

def norm(w):
    w = unicodedata.normalize('NFKD', w.lower())
    return re.sub(r'[^a-z0-9%]', '', ''.join(c for c in w if not unicodedata.combining(c)))

def sec(t):
    h, m, r = t.strip().split(':'); s, ms = re.split('[,.]', r)
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# Decode with ffmpeg to 16 kHz mono, which sidesteps PyAV version clashes inside faster-whisper.
pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.media, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
model = WhisperModel(a.model, device='cpu', compute_type='int8')
segs, _ = model.transcribe(audio, language=a.lang, word_timestamps=True, vad_filter=True)
heard = [{'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)} for s in segs for w in s.words if w.word.strip()]

if not a.srt:
    out = [dict(x, cue=None, src='whisper') for x in heard]
else:
    cues = []
    for block in re.split(r'\n\s*\n', open(a.srt, encoding='utf-8-sig').read().strip()):
        L = block.strip().splitlines()
        if len(L) >= 2 and '-->' in L[1]:
            s0, s1 = (sec(x) for x in L[1].split('-->'))
            cues.append((int(L[0]), s0, s1, ' '.join(L[2:]).split()))
    cues.sort(key=lambda c: c[1])  # CapCut exports can list cues out of order
    script = [(c[0], w) for c in cues for w in c[3]]
    sm = difflib.SequenceMatcher(None, [norm(w) for _, w in script], [norm(x['w']) for x in heard], autojunk=False)
    times = [None] * len(script)
    for op, i0, i1, j0, j1 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i1 - i0):
                times[i0 + k] = (heard[j0 + k]['s'], heard[j0 + k]['e'])
        elif op == 'replace':  # same place, heard differently ("Cloud" for "Claude"): spread Whisper's span over the SRT words
            n, m = i1 - i0, j1 - j0
            for k in range(n):
                a0, a1 = j0 + k * m // n, j0 + max(k * m // n, (k + 1) * m // n - 1)
                times[i0 + k] = (heard[a0]['s'], heard[a1]['e'])
    out, pos = [], 0
    for idx, s0, s1, words in cues:
        span = list(range(pos, pos + len(words))); pos += len(words)
        for k, i in enumerate(span):
            if times[i]:
                out.append({'w': script[i][1], 's': times[i][0], 'e': times[i][1], 'cue': idx, 'src': 'whisper'})
            else:  # spread unmatched words between the nearest known times inside the cue
                prev = next((times[j][1] for j in reversed(span[:k]) if times[j]), s0)
                nxt = next((times[j][0] for j in span[k + 1:] if times[j]), s1)
                gap = [j for j in span if not times[j]]
                f = (gap.index(i) + .5) / len(gap)
                t = round(prev + (nxt - prev) * f, 2)
                out.append({'w': script[i][1], 's': t, 'e': t, 'cue': idx, 'src': 'interp'})

json.dump(out, open(a.out, 'w'), ensure_ascii=False, indent=0)
for x in out:
    print(f"{x['s']:7.2f} {x['e']:7.2f}  {x['w']}" + ('  (interp)' if x['src'] == 'interp' else ''))
matched = sum(x['src'] == 'whisper' for x in out)
print(f'{a.out}: {len(out)} words, {matched} timed by Whisper, {len(out) - matched} interpolated', file=sys.stderr)

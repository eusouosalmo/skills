"""Convert SRT times or seconds to CapCut timecode HH:MM:SS:FF at 30fps.

  python3 timecode.py 00:01:41,066 101.5
  python3 timecode.py --srt narration.srt   # every cue: index, start, end, text
"""
import re, sys

FPS = 30  # CapCut timeline rate for these reels; FF is the frame within the second

def seconds(s):
    m = re.fullmatch(r'(\d+):(\d\d):(\d\d)[,.](\d+)', s.strip())
    if not m and not re.fullmatch(r'[\d.]+', s.strip()): sys.exit(f'not an SRT time or seconds: {s}')
    return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + float('0.' + m[4]) if m else float(s)

def tc(sec):
    f = int(round(sec * FPS))
    return f'{f // (3600 * FPS):02d}:{f // (60 * FPS) % 60:02d}:{f // FPS % 60:02d}:{f % FPS:02d}'

if sys.argv[1:2] == ['--srt']:
    for block in re.split(r'\n\s*\n', open(sys.argv[2], encoding='utf-8-sig').read().strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 2 and '-->' in lines[1]:
            a, b = lines[1].split('-->')
            print(lines[0], tc(seconds(a)), tc(seconds(b)), ' '.join(lines[2:]).strip(), sep='\t')
else:
    for x in sys.argv[1:]: print(x, tc(seconds(x)), sep='\t')

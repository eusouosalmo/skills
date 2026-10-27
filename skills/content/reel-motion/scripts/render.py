"""Render a scene HTML that defines a global render(t) (t in seconds from the scene start).

  python3 render.py stills scene.html 0.5 3.0 [--backdrop frame.png] [--out stills/]
  python3 render.py video  scene.html DURATION out.mov --alpha
  python3 render.py video  scene.html DURATION out.mp4

stills: one PNG per time, composited over --backdrop (a frame of the author's recording) when given.
video --alpha: transparent overlay as QuickTime Animation (.mov, qtrle). Without --alpha: opaque H.264 .mp4.
1080x1920, 30fps, no audio. If the page defines window.swap(t) (async), it is awaited each frame.
"""
import argparse, os, shutil, subprocess, sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit('playwright missing: run bash scripts/setup.sh')
if not shutil.which('ffmpeg'):
    sys.exit('ffmpeg not found on PATH: run bash scripts/setup.sh')

W, H, FPS = 1080, 1920, 30  # vertical Reels/Shorts frame and the CapCut timeline rate

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['stills', 'video'])
ap.add_argument('html')
ap.add_argument('rest', nargs='+')
ap.add_argument('--alpha', action='store_true')
ap.add_argument('--backdrop')
ap.add_argument('--out', default='stills')
a = ap.parse_args()

STEP = "async t=>{render(t);if(window.swap)await window.swap(t)}"
# Replays 0..t so state that builds up frame by frame is right in a still.
REPLAY = "async t=>{for(let x=0;x<t;x+=1/30)render(x);render(t);if(window.swap)await window.swap(t)}"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H})
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.abspath(a.html))
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)  # lets web fonts and images settle after fonts.ready
    if a.mode == 'stills':
        os.makedirs(a.out, exist_ok=True)
        for t in map(float, a.rest):
            pg.evaluate(REPLAY, t)
            path = os.path.join(a.out, f's_{t:06.2f}.png')
            pg.screenshot(path=path, omit_background=True)
            if a.backdrop:  # composite over the recording frame with ffmpeg, scaled to 1080x1920
                comp = path.replace('.png', '_over.png')
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a.backdrop, '-i', path, '-filter_complex',
                                f'[0]scale={W}:{H}[b];[b][1]overlay', '-frames:v', '1', comp], check=True)
                path += ' ' + comp
            print(path)
    else:
        dur, out = float(a.rest[0]), a.rest[1]
        # qtrle is the alpha codec that kept transparency in CapCut; -g 90 adds a keyframe every 3 s,
        # which keeps the file small (a single keyframe for the whole clip inflates it).
        enc = (['-c:v', 'qtrle', '-pix_fmt', 'argb', '-g', '90'] if a.alpha else
               ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'])
        if a.alpha and not out.endswith('.mov'): sys.exit('--alpha writes QuickTime Animation: use a .mov output')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
                               '-c:v', 'png', '-i', '-', '-an', *enc, out], stdin=subprocess.PIPE)
        n = int(round(dur * FPS))
        for i in range(n):
            pg.evaluate(STEP, i / FPS)
            ff.stdin.write(pg.screenshot(type='png', omit_background=a.alpha))
        ff.stdin.close(); ff.wait(); print(out, n, 'frames')
    if errs: print('page errors:', errs, file=sys.stderr)
    b.close()

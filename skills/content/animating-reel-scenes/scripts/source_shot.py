"""Capture the primary source of an on-screen fact, with the box of the quoted passage, for a source-shot scene.

  python3 source_shot.py "https://www.postgresql.org/docs/current/datatype-json.html" \
      "supports queries with the key-exists operators" -o assets/fonte-postgres

Writes <out>.png (the page at 1080 px wide, cropped around the quote) and <out>.json with the quote's
rectangles inside that image ({"url", "quote", "width", "height", "rects": [{x, y, w, h}, ...]}), one rect per
line the quote wraps to. The scene shows the image and grows a highlight over those rects on the spoken word.
The quote must appear on the page as written (same words, any spacing); the script exits if it does not.
"""
import argparse, json, sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit('playwright missing: run bash scripts/setup.sh')

ap = argparse.ArgumentParser()
ap.add_argument('url'); ap.add_argument('quote'); ap.add_argument('-o', '--out', required=True)
ap.add_argument('--height', type=int, default=1100, help='crop height around the quote, in output px')
ap.add_argument('--zoom', type=float, default=2, help='page scale; 2 makes body text readable on a phone')
a = ap.parse_args()

FIND = """q => {
  const want = q.replace(/\\s+/g, ' ').trim().toLowerCase();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; let text = '';
  while (walker.nextNode()) { const n = walker.currentNode; nodes.push([n, text.length]); text += n.data; }
  const flat = text.replace(/\\s+/g, ' ').toLowerCase();
  // map positions of the whitespace-collapsed text back to the raw text
  const map = []; let prevSpace = false;
  for (let i = 0; i < text.length; i++) { const sp = /\\s/.test(text[i]); if (sp && prevSpace) continue; map.push(i); prevSpace = sp; }
  const at = flat.indexOf(want);
  if (at < 0) return null;
  const s = map[at], e = map[at + want.length - 1] + 1;
  const pick = pos => { for (let k = nodes.length - 1; k >= 0; k--) if (nodes[k][1] <= pos) return [nodes[k][0], pos - nodes[k][1]]; };
  const r = document.createRange(); const [sn, so] = pick(s), [en, eo] = pick(e - 1);
  r.setStart(sn, so); r.setEnd(en, eo + 1);
  return [...r.getClientRects()].map(x => ({x: x.left, y: x.top + scrollY, w: x.width, h: x.height}));
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    z = a.zoom
    pg = b.new_page(viewport={'width': int(1080 / z), 'height': int(1920 / z)}, device_scale_factor=z)
    pg.goto(a.url, wait_until='networkidle')
    # Measure and shoot at the full page height, so nothing reflows between the two (a full_page screenshot resizes the viewport).
    full = pg.evaluate('document.documentElement.scrollHeight')
    pg.set_viewport_size({'width': int(1080 / z), 'height': min(full, 16000)})
    rects = pg.evaluate(FIND, a.quote)
    if not rects:
        sys.exit(f'quote not found on {a.url}: copy it from the page exactly')
    top = max(0, min(r['y'] for r in rects) - a.height / z / 3)  # CSS px; the quote sits in the upper third
    pg.screenshot(path=a.out + '.png', clip={'x': 0, 'y': top, 'width': 1080 / z, 'height': a.height / z})
    rel = [{k: round((v - (top if k == 'y' else 0)) * z, 1) for k, v in r.items()} for r in rects]  # output px
    json.dump({'url': a.url, 'quote': a.quote, 'width': 1080, 'height': a.height, 'rects': rel}, open(a.out + '.json', 'w'), indent=1)
    b.close()
print(a.out + '.png', len(rel), 'line(s)')

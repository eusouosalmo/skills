"""Share of the stage's width and height that a still's content spans.

Usage: python3 width.py still.png [still.png ...] [--panel]
The background is the most common colour; the caption band (0.68 to 0.80 of the height)
is masked. With --panel, only the top 1080x960 half is measured.
"""
import sys, numpy as np
from PIL import Image
panel = '--panel' in sys.argv
for p in [a for a in sys.argv[1:] if a != '--panel']:
    im = np.asarray(Image.open(p).convert('RGB').resize((270, 480))).astype(int)
    if panel: im = im[:240]
    q = (im // 16).reshape(-1, 3); keys = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    bg = np.bincount(keys).argmax(); bgc = np.array([bg // 256, (bg // 16) % 16, bg % 16]) * 16 + 8
    d = np.abs(im - bgc).sum(2) > 60
    if not panel: d[int(480 * 0.68):int(480 * 0.80)] = False
    cols = np.where(d.mean(0) > 0.02)[0]; rows = d.mean(1) > 0.02
    width = (cols[-1] - cols[0] + 1) / d.shape[1] if len(cols) else 0
    centre = (cols[0] + cols[-1]) / 2 / d.shape[1] if len(cols) else 0
    print(f"{p} width={width:.2f} centre_x={centre:.2f} height={rows.mean():.2f}")

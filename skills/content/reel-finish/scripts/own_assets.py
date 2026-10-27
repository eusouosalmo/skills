"""Our own versions of what the mp4 takes from the CapCut cache: free fonts close to the reference project's
caption and word fonts, and synthesized versions of its library sounds. Used when the cache lacks a file (another
machine, a cleared cache) or when the plan asks for them ("own_assets": true), so the mp4 never depends on
material that is CapCut's to license.

Fonts come from Google Fonts (SIL Open Font License), downloaded once into ~/.cache/reel-finish/fonts.
Sounds are synthesized with numpy into ~/.cache/reel-finish/sounds, from the envelope and spectrum measured
on the CapCut originals.
"""
import sys
import urllib.request
import wave
from pathlib import Path

CACHE = Path.home() / ".cache" / "reel-finish"
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl"

# The CapCut fonts of the author's reference project, measured on the files: capital height over ascent+descent
# (libass sizes a font by ascent+descent) and the advance of "DA TUA CONVERSA" in capital heights. Our font is
# sized and narrowed to these, so the capitals keep CapCut's height and the lines break where CapCut breaks them.
CAPCUT_FONTS = {"ZY Resolve": (0.8014, 12.888), "ZY Modern": (0.6731, 12.626)}
# Our font for each, picked by eye and by overlap of rendered text: Lexend has ZY Resolve's geometric capitals and
# open spacing; Kanit ExtraBold has ZY Modern's heavy, slightly condensed ones.
OWN_FONTS = {"ZY Resolve": ("lexend/Lexend%5Bwght%5D.ttf", 900), "ZY Modern": ("kanit/Kanit-ExtraBold.ttf", None)}
DEFAULT_FONT = ("lexend/Lexend%5Bwght%5D.ttf", 900)
SAMPLE = "DA TUA CONVERSA"


def _metrics(path):
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont
    f = TTFont(path)
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    pen = BoundsPen(gs)
    gs[cmap[ord("H")]].draw(pen)
    cap = pen.bounds[3]
    o = f["OS/2"]  # libass sizes by the win metrics when the font sets them (the ZY fonts have them equal to hhea)
    em = o.usWinAscent + o.usWinDescent or f["hhea"].ascent - f["hhea"].descent
    adv = sum(f["hmtx"][cmap[ord(c)]][0] for c in SAMPLE)
    return cap / em, adv / cap


def font(capcut_name):
    """(path, family, size factor, horizontal scale) of our font standing in for a CapCut font, by its family name."""
    src, weight = OWN_FONTS.get(capcut_name, DEFAULT_FONT)
    stem = Path(src).name.split("%5B")[0]
    stem = stem[:-4] if stem.endswith(".ttf") else stem
    out = CACHE / "fonts" / f"{stem}{'-' + str(weight) if weight else ''}.ttf"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        raw = out.with_suffix(".download.ttf")
        print(f"own_assets: downloading {src} from Google Fonts (OFL)", file=sys.stderr)
        urllib.request.urlretrieve(f"{GF}/{src}", raw)
        if weight:  # a variable font: keep one weight
            from fontTools.ttLib import TTFont
            from fontTools.varLib import instancer
            instancer.instantiateVariableFont(TTFont(raw), {"wght": weight}).save(out)
            raw.unlink()
        else:
            raw.rename(out)
    from fontTools.ttLib import TTFont
    family = TTFont(out)["name"].getDebugName(1)  # libass finds a font in fontsdir by the family inside the file
    ref_cap, ref_width = CAPCUT_FONTS.get(capcut_name, CAPCUT_FONTS["ZY Resolve"])
    cap, width = _metrics(out)
    return out, family, ref_cap / cap, ref_width / width


def _write(path, x, sr=48000):
    import numpy as np
    x = np.clip(x, -1, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def _shutter(sr):
    """Camera shutter: three bright mechanical ticks between 40 and 100 ms, gone by 200 ms (centroid ~7 kHz)."""
    import numpy as np
    rng = np.random.default_rng(1)
    t = np.arange(int(0.3 * sr)) / sr
    x = np.zeros_like(t)
    for at, amp in ((0.035, 0.6), (0.075, 0.8), (0.10, 1.0)):
        k = t >= at
        x[k] += amp * rng.standard_normal(k.sum()) * np.exp(-(t[k] - at) / 0.012)
    return np.diff(x, prepend=0) * 0.9  # the derivative tilts the noise up, as in the original's spectrum


def _reverse_whoosh(sr):
    """Reversed cymbal ("Keen"): noise swelling for 1.0 s (about 45 dB), then a short fall (centroid ~6 kHz)."""
    import numpy as np
    rng = np.random.default_rng(2)
    n = int(1.367 * sr)
    t = np.arange(n) / sr
    env = np.where(t < 1.0, 10 ** ((-45 + 45 * (t / 1.0) ** 1.6) / 20), 10 ** ((-18 - 120 * (t - 1.0)) / 20))
    x = np.diff(rng.standard_normal(n), prepend=0) * 0.5
    return x * env * 0.17  # peak about -15 dBFS, like the original


def _click(sr):
    """Mouse click: press at 10 ms and release at 90 ms, short and bright (centroid ~8 kHz)."""
    import numpy as np
    rng = np.random.default_rng(3)
    t = np.arange(int(0.1333 * sr)) / sr
    x = np.zeros_like(t)
    for at, amp in ((0.01, 0.6), (0.09, 0.8)):
        k = t >= at
        x[k] += amp * rng.standard_normal(k.sum()) * np.exp(-(t[k] - at) / 0.003)
    return np.diff(x, prepend=0)


SOUNDS = {"shutter": _shutter, "reverse": _reverse_whoosh, "click": _click}


def sound(capcut_name):
    """Path to our synthesized stand-in for a CapCut library sound, by its name, or None when there is none."""
    n = capcut_name.lower()
    kind = ("shutter" if "shutter" in n or "camera" in n else "reverse" if "reverse" in n or "keen" in n
            else "click" if "click" in n or "鼠标" in n else None)
    if kind is None:
        return None
    out = CACHE / "sounds" / f"{kind}.wav"
    if not out.exists():
        _write(out, SOUNDS[kind](48000))
    return out

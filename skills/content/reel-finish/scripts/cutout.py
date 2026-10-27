"""Cuts the person out of the recording, as a .mov with alpha, for the words that sit behind the head.

The reference project puts a copy of the recording with CapCut's background removal over its words, so the hair
covers them. CapCut keeps that cut-out in its own mask format inside the project; this script makes the same layer as a
QuickTime Animation .mov, which CapCut and the mp4 both lay over the words.

Used by assemble_draft.py and render_mp4.py; not run by hand. Requires numpy, Pillow and mediapipe:
    .venv/bin/pip install numpy pillow mediapipe
The segmentation model (MediaPipe selfie segmenter, Apache 2.0, 250 KB) is downloaded once into ~/.cache/reel-finish.
"""
import subprocess
import urllib.request
from pathlib import Path

W, H, FPS = 1080, 1920, 30
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/"
             "selfie_segmenter.tflite")
MODEL = Path.home() / ".cache" / "reel-finish" / "selfie_segmenter.tflite"
# The model's confidence is soft at the hair; mapping 0.25..0.75 to 0..1 keeps the hair edge without a halo
# (checked on the author's two reels, light and dark backgrounds).
EDGE = (0.25, 0.75)


def render(rec, out, t0, t1, scale_at, die):
    """Writes frames t0..t1 of rec, zoomed as scale_at(t) gives (the punch-ins), with alpha outside the person."""
    try:
        import mediapipe as mp
        import numpy as np
        from mediapipe.tasks.python import BaseOptions, vision
        from PIL import Image
    except ImportError:
        die("words behind the head need numpy, pillow and mediapipe: .venv/bin/pip install numpy pillow mediapipe")
    if not MODEL.exists():
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(MODEL_URL, MODEL)
        except OSError as e:
            die(f"cannot download the segmentation model from {MODEL_URL}: {e}")
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL)), output_confidence_masks=True))
    n = round((t1 - t0) * FPS)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t0:.4f}", "-i", str(rec), "-frames:v", str(n),
                          "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if raw.returncode:
        die(f"ffmpeg could not read {rec} at {t0:.2f} s")
    frames = np.frombuffer(raw.stdout, np.uint8).reshape(-1, H, W, 3)
    out.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", "-pix_fmt", "argb", str(out)],
                           stdin=subprocess.PIPE)
    for i, f in enumerate(frames):
        s = scale_at(t0 + i / FPS)
        if s != 1.0:  # the same zoom as the punch-in, around the frame centre
            cw, ch = W / s, H / s
            f = np.asarray(Image.fromarray(f).resize((W, H), Image.BILINEAR,
                                                     box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)))
        m = np.squeeze(seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)))
                       .confidence_masks[0].numpy_view())
        a = np.clip((m - EDGE[0]) / (EDGE[1] - EDGE[0]), 0, 1)
        enc.stdin.write(np.dstack([f, (a * 255).astype(np.uint8)]).tobytes())
    enc.stdin.close()
    if enc.wait():
        die(f"ffmpeg could not write {out}")
    seg.close()

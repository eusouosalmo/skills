"""Compose a split-screen export: the rendered scene's top half over the author's face from the recording.

  python3 split.py exports/NN-name-top.mp4 recording.mp4 --start 34.67 --face-y 520 -o exports/NN-name.mp4

The scene is rendered as usual at 1080x1920 with its content in the top half (y 0 to 960). The bottom half
of the export is a 1080x960 crop of the recording over the same stretch, from --face-y down, so the face keeps
the timing of the speech. Pick --face-y from a recording frame: a little above the top of the head.
Silent output; the speech stays on the recording's own track in CapCut.
"""
import argparse, shutil, subprocess, sys

if not shutil.which('ffmpeg'): sys.exit('ffmpeg not found on PATH: run bash scripts/setup.sh')
ap = argparse.ArgumentParser()
ap.add_argument('scene'); ap.add_argument('recording')
ap.add_argument('--start', type=float, required=True, help='scene start on the recording clock, in seconds')
ap.add_argument('--face-y', type=int, required=True, help='top of the 960 px crop on the 1080x1920 recording')
ap.add_argument('-o', '--out', required=True)
a = ap.parse_args()
if not 0 <= a.face_y <= 960: sys.exit('--face-y must be between 0 and 960 so the crop stays inside the frame')
dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.scene],
                     capture_output=True, text=True, check=True).stdout.strip()
f = (f"[0:v]crop=1080:960:0:0[top];"
     f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=1080:960:0:{a.face_y},fps=30[face];"
     f"[top][face]vstack=2[v]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.scene, '-ss', str(a.start), '-t', dur, '-i', a.recording,
                '-filter_complex', f, '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', a.out], check=True)
print(a.out)

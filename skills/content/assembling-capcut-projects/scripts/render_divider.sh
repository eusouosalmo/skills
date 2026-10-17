#!/usr/bin/env bash
# render_divider.sh <out.mov> <duration-s> [panel-bottom-px=960] [draw-in-s=0.4]
# Renders the split-screen divider as a 1080x1920 overlay with real alpha: a black line 10 px tall with a
# hard shadow 14 px tall at 35% under it, drawn from the centre to both edges in draw-in-s.
# Why geq and pad: ffmpeg drawbox does not write alpha, so the strip is computed pixel by pixel and padded
# into a transparent full frame. qtrle/argb keeps the alpha in a .mov that CapCut reads.
set -euo pipefail
out=${1:?out.mov}; dur=${2:?duration}; bottom=${3:-960}; ramp=${4:-0.4}
command -v ffmpeg >/dev/null || { echo "render_divider: ffmpeg not found" >&2; exit 1; }
top=$((bottom - 4))   # the line straddles the panel edge: 4 px over the panel, 6 px over the video
ffmpeg -nostdin -v error -y -f lavfi -i "color=c=black:s=1080x24:r=30:d=$dur,format=rgba" \
  -vf "geq=r=0:g=0:b=0:a='if(lt(abs(X-540),540*min(1,T/$ramp)),if(lt(Y,10),255,89),0)',pad=1080:1920:0:$top:color=black@0,format=rgba" \
  -c:v qtrle -pix_fmt argb "$out"
echo "render_divider: wrote $out ($dur s, line at y $top)"

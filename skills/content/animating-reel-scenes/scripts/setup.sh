#!/usr/bin/env bash
# Checks what render.py and timecode.py need: python3, the playwright package, its Chromium, and ffmpeg.
#
#   bash setup.sh            # check only, print the install command for anything missing
#   bash setup.sh --install  # also run those commands, asking before each one
#
# Playwright goes into its own virtualenv (~/.venvs/reel-scenes) because Debian, Ubuntu and
# Homebrew Python refuse a global pip install (PEP 668). Run the scripts with that venv's python.
set -uo pipefail

VENV="${REEL_VENV:-$HOME/.venvs/reel-scenes}"
INSTALL=0; [ "${1:-}" = "--install" ] && INSTALL=1

case "$(uname -s)" in
  Darwin) OS=mac ;;
  Linux) OS=linux ;;
  MINGW*|MSYS*|CYGWIN*) OS=windows ;;
  *) OS=other ;;
esac

missing=0
ok()   { printf '  ok       %s\n' "$1"; }
miss() { printf '  missing  %s\n           %s\n' "$1" "$2"; missing=1; }
run()  {
  [ "$INSTALL" = 1 ] || return 1
  printf 'Run: %s ? [y/N] ' "$1"; read -r ans
  [ "$ans" = y ] || [ "$ans" = Y ] || return 1
  bash -c "$1"
}

ffmpeg_cmd() {
  case "$OS" in
    mac) echo "brew install ffmpeg" ;;
    linux) echo "sudo apt-get install -y ffmpeg   # or: sudo dnf install ffmpeg" ;;
    windows) echo "winget install Gyan.FFmpeg" ;;
    *) echo "install ffmpeg from https://ffmpeg.org/download.html" ;;
  esac
}

echo "Checking prerequisites ($OS):"

if command -v python3 >/dev/null; then ok "python3 $(python3 -c 'import sys;print(sys.version.split()[0])')"
else miss python3 "install Python 3 from https://www.python.org/downloads/"; fi

if command -v ffmpeg >/dev/null; then ok "ffmpeg"
else miss ffmpeg "$(ffmpeg_cmd)"; run "$(ffmpeg_cmd | sed 's/ *#.*//')" && ok ffmpeg; fi

# Prefer a python that already has playwright; otherwise the venv.
PY=""
for cand in python3 "$VENV/bin/python"; do
  if [ -x "$(command -v "$cand" 2>/dev/null)" ] && "$cand" -c 'import playwright' 2>/dev/null; then PY="$cand"; break; fi
done
if [ -n "$PY" ]; then ok "playwright ($PY)"
else
  cmd="python3 -m venv '$VENV' && '$VENV/bin/pip' install playwright"
  miss "playwright (python package)" "$cmd"
  run "$cmd" && PY="$VENV/bin/python" && ok "playwright ($PY)"
fi

if [ -n "$PY" ]; then
  if "$PY" -c 'from playwright.sync_api import sync_playwright
p = sync_playwright().start(); p.chromium.launch().close(); p.stop()' 2>/dev/null; then ok "chromium for playwright"
  else
    # --with-deps also installs the system libraries Chromium needs on Linux (asks for sudo).
    cmd="'$PY' -m playwright install chromium"; [ "$OS" = linux ] && cmd="'$PY' -m playwright install --with-deps chromium"
    miss "chromium for playwright" "$cmd"
    run "$cmd" && ok "chromium for playwright"
  fi
fi

# faster-whisper times each spoken word for scripts/transcribe.py; it lives in the same venv.
WPY=""
for cand in python3 "$VENV/bin/python"; do
  if [ -x "$(command -v "$cand" 2>/dev/null)" ] && "$cand" -c 'import faster_whisper' 2>/dev/null; then WPY="$cand"; break; fi
done
if [ -n "$WPY" ]; then ok "faster-whisper ($WPY)"
else
  cmd="[ -x '$VENV/bin/python' ] || python3 -m venv '$VENV'; '$VENV/bin/pip' install faster-whisper"
  miss "faster-whisper (python package, for transcribe.py)" "$cmd"
  run "$cmd" && WPY="$VENV/bin/python" && ok "faster-whisper ($WPY)"
fi

echo
[ -n "$WPY" ] && echo "Transcribe with: $WPY scripts/transcribe.py ..."
if [ "$missing" = 0 ]; then
  echo "All set. Render with: ${PY:-python3} scripts/render.py ..."
elif [ "$INSTALL" = 1 ]; then
  echo "Re-run 'bash setup.sh' to confirm everything is in place."
else
  echo "Install what is missing with the commands above, or run: bash setup.sh --install"
fi

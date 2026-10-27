#!/usr/bin/env bash
# Runs a command with a memory ceiling sized to this machine, so a runaway ffmpeg or Whisper dies alone
# instead of freezing the system.
#
#   bash scripts/run_capped.sh ffmpeg -i in.mov ...
#
# Ceiling: 70% of the memory available right now, leaving at least 2 GB to the rest of the system.
# MEMORY_CAP_MB overrides it. Linux and WSL with systemd use a systemd-run scope (swap off for the scope,
# because a WSL VM that starts swapping hard freezes like one out of memory); without systemd, prlimit caps
# the address space. On macOS and Windows the command runs as is: their memory managers kill or page a single
# process without taking the system down, which a WSL VM does not do.
set -euo pipefail
[ $# -gt 0 ] || { echo "usage: run_capped.sh <command> [args...]" >&2; exit 2; }

if [ "$(uname -s)" != "Linux" ]; then
  exec "$@"
fi

avail_mb=$(awk '/MemAvailable/ {print int($2 / 1024)}' /proc/meminfo)
cap_mb=${MEMORY_CAP_MB:-$(( avail_mb * 70 / 100 ))}
max_mb=$(( avail_mb - 2048 ))
if [ -z "${MEMORY_CAP_MB:-}" ] && [ "$cap_mb" -gt "$max_mb" ]; then cap_mb=$max_mb; fi
# Under 1 GB, ffmpeg decoding a 4K HEVC clip or Whisper loading a model would die at once; better to say so.
if [ "$cap_mb" -lt 1024 ]; then
  echo "run_capped: only ${avail_mb} MB available; close something before running heavy work" >&2
  exit 1
fi

if command -v systemd-run >/dev/null && systemctl --user show-environment >/dev/null 2>&1; then
  exec systemd-run --user --scope -q -p MemoryMax="${cap_mb}M" -p MemorySwapMax=0 "$@"
elif command -v prlimit >/dev/null; then
  exec prlimit --as=$(( cap_mb * 1024 * 1024 )) "$@"
else
  echo "run_capped: no systemd-run or prlimit; running without a cap" >&2
  exec "$@"
fi

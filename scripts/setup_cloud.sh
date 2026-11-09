#!/usr/bin/env bash
# Bootstrap Ubuntu/Debian cloud workers without depending on a desktop path.
set -euo pipefail
artmath_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$artmath_root"
artmath_mode="${1:-setup}"
if [[ $# -gt 1 ]] || [[ "$artmath_mode" != setup && "$artmath_mode" != --check && "$artmath_mode" != --smoke-test ]]; then
  echo 'Usage: bash scripts/setup_cloud.sh [--check|--smoke-test]' >&2
  exit 2
fi

if [[ "$artmath_mode" != --check ]]; then
  artmath_python="${ARTMATH_PYTHON:-}"
  if [[ -z "$artmath_python" ]]; then
    for candidate in python3.11 python3.12 python3; do
      if command -v "$candidate" >/dev/null && "$candidate" -c 'import sys; sys.exit(sys.version_info[:2] not in [(3,11),(3,12)])' 2>/dev/null; then
        artmath_python="$candidate"
        break
      fi
    done
  fi
  if [[ -z "$artmath_python" ]] || ! "$artmath_python" -c 'import sys; sys.exit(sys.version_info[:2] not in [(3,11),(3,12)])'; then
    echo 'Install Python 3.11 or 3.12, or set ARTMATH_PYTHON to its executable.' >&2
    exit 2
  fi

  artmath_has_font=false
  for font in assets/fonts/NotoSansThai-ExtraBold.ttf /usr/share/fonts/truetype/noto/NotoSansThai-ExtraBold.ttf /usr/share/fonts/truetype/noto/NotoSansThai-Bold.ttf; do
    if [[ -f "$font" ]]; then artmath_has_font=true; break; fi
  done
  if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null || [[ "$artmath_has_font" == false ]]; then
    artmath_admin=()
    if [[ "$(id -u)" != 0 ]]; then
      if command -v sudo >/dev/null && sudo -n true 2>/dev/null; then
        artmath_admin=(sudo -n)
      else
        echo 'System dependencies missing. Prepare the cloud image with: apt-get install -y ffmpeg fonts-noto-core' >&2
        exit 2
      fi
    fi
    if ! command -v apt-get >/dev/null; then
      echo 'Automatic system installation supports Ubuntu/Debian only. Install FFmpeg/FFprobe and Noto Sans Thai manually.' >&2
      exit 2
    fi
    "${artmath_admin[@]}" apt-get update
    "${artmath_admin[@]}" apt-get install -y ffmpeg fonts-noto-core
  fi

  if [[ ! -x .venv/bin/python ]]; then
    if ! "$artmath_python" -m venv .venv; then
      echo 'Could not create .venv. Install the venv package for your Python version and retry; existing files are not deleted.' >&2
      exit 2
    fi
  fi
  .venv/bin/python -c 'import sys; assert sys.version_info[:2] in [(3,11),(3,12)], "Existing .venv must use Python 3.11 or 3.12"'
  .venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
fi

if [[ ! -x .venv/bin/python ]]; then
  echo 'No .venv found. Run bash scripts/setup_cloud.sh first.' >&2
  exit 2
fi
.venv/bin/python - <<'PY'
import importlib.metadata
import importlib.util
from pathlib import Path
import subprocess
import sys
from PIL import ImageFont

try:
    if sys.version_info[:2] not in [(3, 11), (3, 12)]:
        raise ValueError('Python 3.11 or 3.12 is required')
    expected = Path('requirements.txt').read_text().strip().split('==')[1]
    if importlib.metadata.version('Pillow') != expected:
        raise ValueError('Pillow version does not match requirements.txt; rerun setup')
    spec = importlib.util.spec_from_file_location('artmath_cli', 'tools/dm_project.py')
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    font = cli.find_font()
    ImageFont.truetype(str(font), 82)
    for program in ('ffmpeg', 'ffprobe'):
        subprocess.run([program, '-version'], check=True, capture_output=True)
    for flag, names in [('-filters', ('ass', 'loudnorm', 'sidechaincompress', 'silenceremove', 'unsharp')),
                        ('-encoders', ('libx264', 'aac', 'libmp3lame'))]:
        output = subprocess.check_output(['ffmpeg', '-hide_banner', flag], text=True, stderr=subprocess.STDOUT)
        available = {line.split()[1] for line in output.splitlines() if len(line.split()) >= 2}
        missing = set(names) - available
        if missing:
            raise ValueError(f'FFmpeg lacks {sorted(missing)}')
    print(f'ARTMATH_ENV_OK: Python {sys.version.split()[0]}, Pillow {expected}, FFmpeg/FFprobe, Thai font: {font}')
except (OSError, ValueError, subprocess.CalledProcessError) as exc:
    print(f'Environment check failed: {exc}', file=sys.stderr)
    sys.exit(2)
PY

if [[ "$artmath_mode" == --smoke-test ]]; then
  mkdir -p .local
  artmath_demo="$(mktemp -d "$artmath_root/.local/cloud-smoke.XXXXXXXX")"
  .venv/bin/python examples/create_demo.py --dest "$artmath_demo"
  .venv/bin/python tools/dm_project.py validate "$artmath_demo"
  .venv/bin/python tools/dm_project.py render "$artmath_demo"
  echo "ARTMATH_SMOKE_OK: $artmath_demo/outputs/ArtMath_Final_1080p.mp4"
  echo 'Synthetic results remain local/ignored; upload or export explicitly if needed.'
fi

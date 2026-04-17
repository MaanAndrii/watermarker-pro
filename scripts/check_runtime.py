#!/usr/bin/env python3
"""Runtime smoke-check for Raspberry Pi deployment."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        import streamlit  # noqa: F401
        import PIL  # noqa: F401
        import watermarker_engine as engine
        import config
    except Exception as exc:
        print(f"[FAIL] import error: {exc}")
        return 1

    print("[OK] Core imports successful")
    print(f"[INFO] HEIC support: {engine.is_heic_available()}")
    print(f"[INFO] SVG support: {engine.is_svg_available()}")
    print(f"[INFO] MAX_THREADS={config.MAX_THREADS} DEFAULT_THREADS={config.DEFAULT_THREADS}")
    print(f"[INFO] WORK_DIR={config.get_work_dir()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

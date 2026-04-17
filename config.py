"""
Watermarker Pro v8.0 - Configuration Module
============================================
Centralized configuration and constants
"""

import os
from pathlib import Path

# === APPLICATION INFO ===
APP_VERSION = "8.0"
APP_NAME = "Watermarker Pro"
APP_AUTHOR = "Marynyuk Andriy"
APP_LICENSE = "Proprietary"
APP_REPO = "https://github.com/MaanAndrii"

# === FILE SETTINGS ===
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_FILENAME_LENGTH = 255

# Input: jpg/png/webp/heic/heif — звичайні растрові формати
# SVG підтримується лише як вотермарка, не як вхідне фото
SUPPORTED_INPUT_FORMATS = ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif']
SUPPORTED_OUTPUT_FORMATS = ['JPEG', 'WEBP', 'PNG']

# Підтримувані формати вотермарки (растр + вектор)
SUPPORTED_WATERMARK_FORMATS = ['png', 'svg']

# === IMAGE PROCESSING ===
MAX_IMAGE_DIMENSION = 10000     # Maximum width or height
MIN_IMAGE_DIMENSION = 10
THUMBNAIL_SIZE = (300, 300)
PROXY_IMAGE_WIDTH = 700

# === WATERMARK ===
MIN_WATERMARK_SCALE = 5
MAX_WATERMARK_SCALE = 100
MIN_OPACITY = 0.1
MAX_OPACITY = 1.0
DEFAULT_TEXT_SIZE_PT = 100

# === FONT CACHE ===
FONT_CACHE_MAX_SIZE = 100       # Максимум записів у LRU-кеші шрифтів

# === ASPECT RATIOS ===
ASPECT_RATIOS = {
    "Free / Вільний": None,
    "1:1 (Square)": (1, 1),
    "3:2": (3, 2),
    "4:3": (4, 3),
    "5:4": (5, 4),
    "16:9": (16, 9),
    "9:16": (9, 16)
}

# === DEFAULT SETTINGS ===
DEFAULT_SETTINGS = {
    'resize_val': 1920,
    'wm_pos': 'bottom-right',
    'wm_scale': 15,
    'wm_opacity': 1.0,
    'wm_margin': 15,
    'wm_gap': 30,
    'wm_angle': 0,
    'wm_text': '',
    'wm_text_color': '#FFFFFF',
    'out_fmt': 'JPEG',
    'out_quality': 80,
    'naming_mode': 'Keep Original',
    'naming_prefix': '',
    'font_name': None,
    'preset_wm_bytes': None
}

# === POSITION PRESETS ===
TILED_SETTINGS = {
    'wm_scale': 15,
    'wm_opacity': 0.3,
    'wm_gap': 30,
    'wm_angle': 45
}

CORNER_SETTINGS = {
    'wm_scale': 15,
    'wm_opacity': 1.0,
    'wm_margin': 15,
    'wm_angle': 0
}

# === PERFORMANCE ===
MIN_THREADS = 1
MAX_THREADS = 8
CACHE_TTL = 300  # seconds


def _read_int_env(name: str, default: int, min_value: int = None, max_value: int = None) -> int:
    """Read integer from env with optional bounds and fallback."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
    return value


CPU_COUNT = os.cpu_count() or 1
# Conservative default for Raspberry Pi-class hardware
AUTO_DEFAULT_THREADS = max(MIN_THREADS, min(4, CPU_COUNT))
DEFAULT_THREADS = _read_int_env("WM_DEFAULT_THREADS", AUTO_DEFAULT_THREADS, MIN_THREADS, MAX_THREADS)

# Optional runtime overrides for constrained devices
MAX_FILE_SIZE = _read_int_env("WM_MAX_FILE_SIZE_MB", MAX_FILE_SIZE // (1024 * 1024), 1) * 1024 * 1024
MAX_IMAGE_DIMENSION = _read_int_env("WM_MAX_IMAGE_DIMENSION", MAX_IMAGE_DIMENSION, MIN_IMAGE_DIMENSION, 20000)
MAX_THREADS = _read_int_env("WM_MAX_THREADS", MAX_THREADS, MIN_THREADS, 32)
DEFAULT_THREADS = min(DEFAULT_THREADS, MAX_THREADS)

# === PATHS ===
def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent

def get_assets_dir() -> Path:
    """Get assets directory"""
    return get_project_root() / 'assets'

def get_fonts_dir() -> Path:
    """Get fonts directory"""
    return get_assets_dir() / 'fonts'


def get_work_dir() -> Path:
    """
    Base working directory for temporary upload/session folders.
    Defaults to /tmp/wm-pro but can be overridden with WM_WORK_DIR.
    """
    base = os.getenv("WM_WORK_DIR", "/tmp/wm-pro")
    return Path(base)

# === LOGGING ===
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
LOG_FILE = 'watermarker.log'

# === QUALITY PRESETS ===
QUALITY_PRESETS = {
    'Low': 50,
    'Medium': 70,
    'High': 85,
    'Maximum': 95
}

# === RESIZE PRESETS ===
RESIZE_PRESETS = {
    'HD': 1280,
    'FHD': 1920,
    '2K': 2560,
    '4K': 3840
}

"""
Watermarker Pro v8.0 - Session Module
======================================
Ініціалізація та управління Streamlit session state.
Виділено з utils.py для розподілу відповідальності.
"""

import streamlit as st
import tempfile
import threading
import shutil
from datetime import datetime, timedelta

import config
from logger import get_logger

logger = get_logger(__name__)

_session_lock = threading.Lock()
SESSION_DIR_PREFIX = "wm_pro_v8_"
STALE_SESSION_HOURS = 24


def _ensure_work_dir():
    """Create base work directory if missing."""
    work_dir = config.get_work_dir()
    work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir


def cleanup_stale_temp_directories(max_age_hours: int = STALE_SESSION_HOURS):
    """
    Remove stale session directories from the configured work dir.
    Intended for lightweight housekeeping on app start.
    """
    try:
        root = _ensure_work_dir()
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        for p in root.iterdir():
            if not p.is_dir() or not p.name.startswith(SESSION_DIR_PREFIX):
                continue
            mtime = datetime.utcfromtimestamp(p.stat().st_mtime)
            if mtime < cutoff:
                shutil.rmtree(p, ignore_errors=True)
                logger.info(f"Removed stale temp directory: {p}")
    except Exception as e:
        logger.warning(f"Stale temp cleanup failed: {e}")


def init_session_state():
    """Initialize session state with default values"""

    if 'temp_dir' not in st.session_state:
        try:
            cleanup_stale_temp_directories()
            st.session_state['temp_dir'] = tempfile.mkdtemp(
                prefix=SESSION_DIR_PREFIX,
                dir=str(_ensure_work_dir())
            )
            logger.info(f"Temp directory created: {st.session_state['temp_dir']}")
        except Exception as e:
            logger.error(f"Failed to create temp dir: {e}")
            st.session_state['temp_dir'] = tempfile.gettempdir()

    defaults = {
        'file_cache': {},           # fname -> fpath
        'file_order': [],           # упорядкований список fname (drag-and-drop)
        'selected_files': set(),
        'uploader_key': 0,
        'lang_code': 'ua',
        # editing_file, editor_open, close_editor — видалено.
        # @st.dialog викликається напряму всередині if st.button() —
        # жодних прапорців не потрібно.
        'results': None,
        'cancel_token': None,       # CancellationToken | None
        'processing_active': False, # True поки йде batch
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Налаштування (ключі з config.DEFAULT_SETTINGS)
    for key, value in config.DEFAULT_SETTINGS.items():
        key_name = f'{key}_key' if not key.endswith('_val') else f'{key}_state'
        if key_name not in st.session_state:
            st.session_state[key_name] = value


def reset_settings():
    """Reset all settings to defaults"""
    try:
        for key, value in config.DEFAULT_SETTINGS.items():
            key_name = f'{key}_key' if not key.endswith('_val') else f'{key}_state'
            st.session_state[key_name] = value
        logger.info("Settings reset to defaults")
    except Exception as e:
        logger.error(f"Failed to reset settings: {e}")


def safe_state_update(key: str, value):
    """Thread-safe session state update"""
    with _session_lock:
        st.session_state[key] = value


def handle_pos_change():
    """Handle watermark position change with preset application"""
    try:
        position = st.session_state.get('wm_pos_key', 'bottom-right')
        settings = config.TILED_SETTINGS if position == 'tiled' else config.CORNER_SETTINGS
        for key, value in settings.items():
            st.session_state[f'{key}_key'] = value
        logger.debug(f"Position changed to: {position}")
    except Exception as e:
        logger.error(f"Failed to handle position change: {e}")

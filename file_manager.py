"""
Watermarker Pro v8.0 - File Manager
=====================================
Управління тимчасовими файлами, шрифтами та upload-операціями.
Виділено з utils.py для розподілу відповідальності.
"""

import os
import shutil
import tempfile
import streamlit as st
from typing import List, Tuple
from datetime import datetime

import config
from validators import sanitize_filename
from logger import get_logger

logger = get_logger(__name__)


def save_uploaded_file(uploaded_file) -> Tuple[str, str]:
    """
    Save Streamlit UploadedFile to temp directory.

    Returns:
        (file_path, sanitized_filename)
    """
    try:
        temp_dir = st.session_state['temp_dir']
        safe_name = sanitize_filename(uploaded_file.name)
        file_path = os.path.join(temp_dir, safe_name)

        # Handle duplicates
        if os.path.exists(file_path):
            base, ext = os.path.splitext(safe_name)
            ts = datetime.now().strftime("%H%M%S%f")
            safe_name = f"{base}_{ts}{ext}"
            file_path = os.path.join(temp_dir, safe_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        logger.info(f"File saved: {safe_name}")
        return file_path, safe_name

    except Exception as e:
        logger.error(f"Failed to save file {uploaded_file.name}: {e}")
        raise


def cleanup_temp_directory():
    """Clean up temporary directory and recreate it"""
    try:
        temp_dir = st.session_state.get('temp_dir')
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"Temp directory cleaned: {temp_dir}")
        work_dir = config.get_work_dir()
        work_dir.mkdir(parents=True, exist_ok=True)
        st.session_state['temp_dir'] = tempfile.mkdtemp(prefix="wm_pro_v8_", dir=str(work_dir))
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")


def get_available_fonts() -> List[str]:
    """
    Get sorted list of TTF/OTF font filenames from assets/fonts/.

    Returns:
        List of font filenames
    """
    try:
        font_dir = config.get_fonts_dir()
        if not font_dir.exists():
            logger.warning(f"Font directory not found: {font_dir}")
            return []
        fonts = list(font_dir.glob("*.ttf")) + list(font_dir.glob("*.otf"))
        names = sorted(f.name for f in fonts)
        logger.debug(f"Found {len(names)} fonts")
        return names
    except Exception as e:
        logger.error(f"Failed to list fonts: {e}")
        return []

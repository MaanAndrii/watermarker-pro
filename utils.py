"""
Watermarker Pro v8.0 - Utils (facade)
======================================
Цей файл залишається точкою входу для зворотної сумісності,
але вся логіка тепер розподілена між:
  - session.py       — ініціалізація стану, reset
  - preset_manager.py — збереження/завантаження JSON пресетів
  - file_manager.py  — temp-файли, шрифти, upload
  - watermarker_engine.py — підготовка вотермарки
"""

# === RE-EXPORTS ===

from session import (
    init_session_state,
    reset_settings,
    safe_state_update,
    handle_pos_change,
)

from preset_manager import (
    get_current_settings_json,
    apply_settings_from_json,
)

from file_manager import (
    save_uploaded_file,
    cleanup_temp_directory,
    get_available_fonts,
)

# === CSS INJECTION ===

import streamlit as st


def inject_css():
    """Inject custom CSS for UI styling"""
    st.markdown("""
<style>
div[data-testid="column"] {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #eee;
    transition: all 0.2s ease;
}
div[data-testid="column"]:hover {
    border-color: #ff4b4b;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
div[data-testid="column"] button { width: 100%; margin-top: 5px; }
.block-container { padding-top: 2rem; }
.preview-placeholder {
    border: 2px dashed #e0e0e0;
    border-radius: 10px;
    padding: 40px 20px;
    text-align: center;
    color: #888;
    background-color: #fafafa;
    margin-top: 10px;
}
.preview-icon { font-size: 40px; margin-bottom: 10px; display: block; }
</style>
""", unsafe_allow_html=True)


# === WATERMARK PREPARATION ===

import config
import watermarker_engine as engine
from typing import Optional, Dict


def prepare_watermark_object(wm_file, selected_font_name: Optional[str]) -> Optional[object]:
    """
    Prepare watermark object from text, PNG, or SVG.

    Priority:
        1. Текст (wm_text_key)
        2. PNG/SVG файл (wm_file або preset_wm_bytes_key)

    SVG растеризується через engine.load_svg_watermark().
    """
    try:
        wm_text = st.session_state.get('wm_text_key', '').strip()

        if wm_text:
            font_path = None
            if selected_font_name:
                font_path = str(config.get_fonts_dir() / selected_font_name)
            wm_obj = engine.create_text_watermark(
                wm_text,
                font_path,
                config.DEFAULT_TEXT_SIZE_PT,
                st.session_state.get('wm_text_color_key', '#FFFFFF')
            )
            if wm_obj:
                wm_obj = engine.apply_opacity(
                    wm_obj, st.session_state.get('wm_opacity_key', 1.0)
                )
            return wm_obj

        # Файл вотермарки
        wm_bytes = None
        wm_filename = None

        if wm_file:
            wm_bytes = wm_file.getvalue()
            wm_filename = wm_file.name.lower()
        elif st.session_state.get('preset_wm_bytes_key'):
            wm_bytes = st.session_state['preset_wm_bytes_key']
            wm_filename = st.session_state.get('preset_wm_filename_key', 'wm.png')

        if wm_bytes:
            if wm_filename and wm_filename.endswith('.svg'):
                wm_obj = engine.load_svg_watermark(wm_bytes)
            else:
                wm_obj = engine.load_watermark_from_bytes(wm_bytes)

            wm_obj = engine.apply_opacity(
                wm_obj, st.session_state.get('wm_opacity_key', 1.0)
            )
            return wm_obj

        return None

    except Exception as e:
        from logger import get_logger
        get_logger(__name__).error(f"Watermark preparation failed: {e}")
        raise


def get_resize_config() -> Dict:
    """Get current resize and watermark configuration dict"""
    wm_pos = st.session_state.get('wm_pos_key', 'bottom-right')
    return {
        'enabled':    st.session_state.get('resize_enabled', True),
        'mode':       st.session_state.get('resize_mode', 'Max Side'),
        'value':      st.session_state.get('resize_val_state', 1920),
        'wm_scale':   st.session_state.get('wm_scale_key', 15) / 100,
        'wm_margin':  st.session_state.get('wm_margin_key', 15) if wm_pos != 'tiled' else 0,
        'wm_gap':     st.session_state.get('wm_gap_key', 30) if wm_pos == 'tiled' else 0,
        'wm_position': wm_pos,
        'wm_angle':   st.session_state.get('wm_angle_key', 0),
    }

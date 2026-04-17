"""
Watermarker Pro v8.0 - Preset Manager
======================================
Збереження та завантаження JSON-пресетів.
Виділено з utils.py для розподілу відповідальності.
"""

import json
import streamlit as st
from typing import Optional, Tuple
from datetime import datetime

import config
import watermarker_engine as engine
from logger import get_logger

logger = get_logger(__name__)


def get_current_settings_json(uploaded_wm_file) -> str:
    """
    Export current settings as JSON string.

    Args:
        uploaded_wm_file: Поточний Streamlit UploadedFile для вотермарки (або None)

    Returns:
        JSON string
    """
    try:
        wm_b64 = None
        if uploaded_wm_file:
            wm_b64 = engine.image_to_base64(uploaded_wm_file.getvalue())
        elif st.session_state.get('preset_wm_bytes_key'):
            wm_b64 = engine.image_to_base64(st.session_state['preset_wm_bytes_key'])

        settings = {
            'version': config.APP_VERSION,
            'created': datetime.now().isoformat(),
            'resize_val': st.session_state.get('resize_val_state', 1920),
            'wm_pos': st.session_state.get('wm_pos_key', 'bottom-right'),
            'wm_scale': st.session_state.get('wm_scale_key', 15),
            'wm_opacity': st.session_state.get('wm_opacity_key', 1.0),
            'wm_margin': st.session_state.get('wm_margin_key', 15),
            'wm_gap': st.session_state.get('wm_gap_key', 30),
            'wm_angle': st.session_state.get('wm_angle_key', 0),
            'wm_text': st.session_state.get('wm_text_key', ''),
            'wm_text_color': st.session_state.get('wm_text_color_key', '#FFFFFF'),
            'font_name': st.session_state.get('font_name_key', None),
            'out_fmt': st.session_state.get('out_fmt_key', 'JPEG'),
            'out_quality': st.session_state.get('out_quality_key', 80),
            'naming_mode': st.session_state.get('naming_mode_key', 'Keep Original'),
            'naming_prefix': st.session_state.get('naming_prefix_key', ''),
            'wm_image_b64': wm_b64
        }

        return json.dumps(settings, indent=4, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Failed to export settings: {e}")
        return "{}"


def apply_settings_from_json(json_file) -> Tuple[bool, Optional[str]]:
    """
    Load settings from JSON preset file.

    Args:
        json_file: Streamlit UploadedFile (.json)

    Returns:
        (success, error_message)
    """
    try:
        data = json.load(json_file)

        if 'version' in data:
            logger.info(f"Loading preset version: {data['version']}")

        mapping = {
            'resize_val':   'resize_val_state',
            'wm_pos':       'wm_pos_key',
            'wm_scale':     'wm_scale_key',
            'wm_opacity':   'wm_opacity_key',
            'wm_margin':    'wm_margin_key',
            'wm_gap':       'wm_gap_key',
            'wm_angle':     'wm_angle_key',
            'wm_text':      'wm_text_key',
            'wm_text_color':'wm_text_color_key',
            'font_name':    'font_name_key',
            'out_fmt':      'out_fmt_key',
            'out_quality':  'out_quality_key',
            'naming_mode':  'naming_mode_key',
            'naming_prefix':'naming_prefix_key',
        }

        for data_key, state_key in mapping.items():
            if data_key in data:
                st.session_state[state_key] = data[data_key]

        if 'wm_image_b64' in data and data['wm_image_b64']:
            try:
                st.session_state['preset_wm_bytes_key'] = engine.base64_to_bytes(
                    data['wm_image_b64']
                )
            except Exception as e:
                logger.warning(f"Failed to load preset watermark: {e}")
                st.session_state['preset_wm_bytes_key'] = None
        else:
            st.session_state['preset_wm_bytes_key'] = None

        logger.info("Preset loaded successfully")
        return True, None

    except json.JSONDecodeError as e:
        msg = f"Invalid JSON format: {e}"
        logger.error(msg)
        return False, msg
    except Exception as e:
        msg = f"Failed to load preset: {e}"
        logger.error(msg)
        return False, msg

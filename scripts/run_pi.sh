#!/usr/bin/env bash
set -euo pipefail

# Tunable limits for Streamlit transport layer (MB).
# NOTE: Streamlit does not support truly "unlimited" uploads/messages.
WM_STREAMLIT_MAX_UPLOAD_MB="${WM_STREAMLIT_MAX_UPLOAD_MB:-1024}"
WM_STREAMLIT_MAX_MESSAGE_MB="${WM_STREAMLIT_MAX_MESSAGE_MB:-1024}"
WM_STREAMLIT_PORT="${WM_STREAMLIT_PORT:-8501}"
WM_STREAMLIT_ADDRESS="${WM_STREAMLIT_ADDRESS:-0.0.0.0}"

exec streamlit run web_app.py \
  --server.address "${WM_STREAMLIT_ADDRESS}" \
  --server.port "${WM_STREAMLIT_PORT}" \
  --server.maxUploadSize "${WM_STREAMLIT_MAX_UPLOAD_MB}" \
  --server.maxMessageSize "${WM_STREAMLIT_MAX_MESSAGE_MB}" \
  --server.headless true

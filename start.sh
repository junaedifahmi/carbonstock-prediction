#!/usr/bin/env sh
# Launch the FastAPI service in the background, then the Streamlit UI in the
# foreground. Hugging Face Spaces routes traffic to $PORT (default 7860),
# which is where Streamlit listens; FastAPI stays internal on port 8000 and is
# called by the UI via $API_URL.
set -e

.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 &

exec .venv/bin/streamlit run demo/streamlit_app.py \
    --server.port "${PORT:-7860}" \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false

FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Hugging Face Spaces runs the container as UID 1000
RUN useradd -m -u 1000 user

WORKDIR /app

# Install dependencies (runtime only, no dev tools) — cached layer
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Hand ownership to the runtime user and make the launcher executable
RUN chmod +x start.sh && chown -R user:user /app

USER user

# HF Spaces routes traffic to $PORT (Streamlit); FastAPI stays internal on 8000
ENV HOME=/home/user \
    PORT=7860 \
    API_URL=http://localhost:8000/predict

EXPOSE 7860

CMD ["./start.sh"]

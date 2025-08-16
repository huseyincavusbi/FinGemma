# Base image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.cache/huggingface \
    LOCAL_MODEL_PATH=/app/.cache/huggingface/hub/models--huseyincavus--gemma-3-270m-finance-merged/snapshots/c4920974123c4e1f9bc0b2b9fccde75bb717bfe0 \
    MODEL_ID=huseyincavus/gemma-3-270m-finance-merged

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge || true

# Copy the local model into the container's HF cache
COPY models/ ./.cache/huggingface/hub/

# Copy application code
COPY app ./app
COPY start.py ./start.py

# Create necessary directories and set permissions
RUN mkdir -p .cache/huggingface/hub && \
    chmod -R 755 .cache/

EXPOSE 7860 8000

ENV PORT=7860 APP_MODE=ui

CMD ["python", "start.py"]

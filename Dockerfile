# ============================================================
# JARVIS - AI Voice Assistant | Dockerfile
# ============================================================
# NOTE: Audio (microphone + TTS) requires Windows host audio
# passthrough via PulseAudio or direct device mapping.
# See docker-compose.yml for the full audio setup.
# ============================================================

FROM python:3.11-slim

# System dependencies for PyAudio, SpeechRecognition & pyttsx3
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    portaudio19-dev \
    libasound2-dev \
    libpulse-dev \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Environment defaults (overridden via .env / docker-compose)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PULSE_SERVER=tcp:host.docker.internal:4713

# Health-check: ensure Python can import the main modules
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import speech_recognition, pyttsx3, requests" || exit 1

CMD ["python", "main.py"]

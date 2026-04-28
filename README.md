# JARVIS - Python AI Voice Assistant 🤖

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-BAT%20Scripts-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A Python-based AI voice assistant powered by **Google Gemini**, capable of web automation, news fetching, music playback, and hands-free voice commands.

---

## Features

- 🎙️ **Voice command recognition** via SpeechRecognition
- 🌐 **Opens websites** (Google, YouTube, WhatsApp, Instagram, ...)
- 🎵 **Plays music** from your local library
- 📰 **Fetches latest news** via NewsAPI
- 🤖 **AI responses** powered by Google Gemini
- 🐳 **Docker ready** – One-Click setup with BAT scripts

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| AI / LLM | Google Gemini API (`google-genai`) |
| Voice Input | SpeechRecognition + PyAudio |
| Voice Output | pyttsx3 |
| News | NewsAPI (`requests`) |
| Containerization | Docker + Docker Compose |
| Config | python-dotenv |

---

## Quick Start (Docker – One Click)

> **Recommended for easy setup.** Requires [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.

### Step 1 – Clone the repository

```bash
git clone https://github.com/StockPro-AI/JARVIS.git
cd JARVIS
```

### Step 2 – Run Setup (once)

```
setup.bat
```

This will:
- Check Docker installation
- Create your `.env` file from `.env.example` and open it in Notepad
- Build the Docker image automatically

### Step 3 – Start JARVIS

```
start.bat
```

### Stop JARVIS

```
stop.bat
```

---

## Manual Setup (without Docker)

> Use this if you want full microphone + TTS support on Windows without Docker.

1. **Clone the repo**
 ```bash
 git clone https://github.com/StockPro-AI/JARVIS.git
 cd JARVIS
 ```

2. **Install dependencies**
 ```bash
 pip install -r requirements.txt
 ```

3. **Create `.env` file** (copy from example)
 ```bash
 copy .env.example .env
 ```
 Then edit `.env` and fill in your API keys:
 ```env
 GEMINI_API_KEY=your_gemini_api_key_here
 NEWS_API_KEY=your_news_api_key_here
 ```

4. **Run JARVIS**
 ```bash
 python main.py
 ```

---

## API Keys

| Key | Where to get it |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `NEWS_API_KEY` | [newsapi.org/register](https://newsapi.org/register) (free tier available) |

---

## Docker Audio Note

JARVIS uses the **microphone** (SpeechRecognition) and **text-to-speech** (pyttsx3). Docker on Windows does not natively support audio devices.

| Option | Description |
|---|---|
| **Option A** (recommended) | Use the manual setup above for full audio support on Windows |
| **Option B** (advanced) | Docker + PulseAudio TCP – see comments in `docker-compose.yml` |

---

## Project Structure

```
JARVIS/
├── main.py              # Main application entry point
├── musiclibrary.py      # Music library definitions
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose one-click setup
├── .env.example         # API key template
├── setup.bat            # Windows: first-time setup
├── start.bat            # Windows: start JARVIS
└── stop.bat             # Windows: stop JARVIS
```

---

## Author

**Madhusudhan BH** – original project

> Docker & one-click setup added by [StockPro-AI](https://github.com/StockPro-AI)

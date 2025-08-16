# FinGemma - Finance LLM Assistant

A containerized finance-focused language model based on Gemma 3 270M, fine-tuned for financial concepts and discussions.

## 🚀 Quick Start

### Using Docker Hub (Recommended)
```bash
# Pull and run the UI (Web Interface)
docker run -p 7860:7860 huseyincavus/fingemma:latest

# Access at: http://localhost:7860
```

### API Mode
```bash
# Pull and run the API
docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest

# Access at: http://localhost:8000
```

## � Features

- **Gradio Web Interface**: Interactive chat interface for finance questions
- **REST API**: Programmatic access with streaming support
- **Finance-Focused**: Fine-tuned on financial concepts, EBITDA, investments, etc.
- **Self-Contained**: Includes the complete model (~550MB) in the container
- **Dual Mode**: Switch between UI and API modes with environment variables

## 🖥️ System Requirements

- Docker installed
- 8GB RAM recommended
- 5GB free disk space

## 📖 Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete installation and deployment instructions for Windows, macOS, and Linux.

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_MODE` | `ui` | `ui` for web interface, `api` for REST API |
| `PORT` | `7860` | Port to run the application |
| `SERVER_NAME` | `127.0.0.1` | Server bind address |

## 📊 API Endpoints

- `GET /health` - Health check
- `POST /generate` - Generate text completion

## 🐳 Docker Hub

Available at: [`huseyincavus/fingemma`](https://hub.docker.com/r/huseyincavus/fingemma)

## 📄 License

This project packages and deploys the Gemma model. Please refer to Google's Gemma license for model usage terms.

# Finance Fine-Tuned Gemma 3 270M UI

This project provides a friendly UI (Gradio) and API (FastAPI) wrapper around the model `huseyincavus/gemma-3-270m-finance-merged` for finance-focused text generation / Q&A.

## Features
- Gradio web UI with streaming and parameter controls
- FastAPI endpoint `/generate` (non-stream & stream)
- Dockerized for Hugging Face Spaces or local deployment

## Quick Start (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app/gradio_app.py  # launches on http://localhost:7860
```

## FastAPI Server (optional)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

POST example:
```bash
curl -X POST http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Explain EBITDA simply","max_new_tokens":128}'
```

## Docker
```bash
docker build -t finance-llm-ui .
docker run -p 7860:7860 finance-llm-ui
```

## Deploy to Hugging Face Space
Space type: Docker
- Repo contains `Dockerfile`
- Set `MODEL_ID` secret/variable if using alternate model

## Environment Variables
| Name | Default | Description |
|------|---------|-------------|
| MODEL_ID | huseyincavus/gemma-3-270m-finance-merged | HF model repo |
| PORT | 7860 | UI port |

## Roadmap / Next Steps
- Add chat history & system prompt
- Add financial document upload & retrieval (RAG)
- Add quant metrics & evaluation notebook

PRs & issues welcome.

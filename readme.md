# FinGemma - Finance LLM Assistant

A containerized finance-focused language model based on Gemma 3 270M, fine-tuned for financial concepts and discussions.

## Quick Start

### Using Multi-Architecture Images (Recommended)

```bash
# Run the web interface (auto-selects your architecture)
docker run -p 7860:7860 huseyincavus/fingemma:latest

# Access at: http://localhost:7860
```

### API Mode

```bash
# Run the API server
docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest

# Access at: http://localhost:8000/docs for Swagger UI
```

## Available Docker Images

| Image | Architecture | Size | Description |
|-------|-------------|------|-------------|
| [`huseyincavus/fingemma:latest`](https://hub.docker.com/repository/docker/huseyincavus/fingemma/general) | Multi-arch | Auto | **Recommended** - Auto-selects AMD64/ARM64 |
| [`huseyincavus/fingemma-amd64:latest`](https://hub.docker.com/repository/docker/huseyincavus/fingemma-amd64/general) | AMD64 | ~5.3GB | Intel/AMD processors, Cloud servers |
| [`huseyincavus/fingemma-arm64:latest`](https://hub.docker.com/repository/docker/huseyincavus/fingemma-arm64/general) | ARM64 | ~4.5GB | Apple Silicon, ARM servers |

## Advanced Usage

### Force Specific Architecture

```bash
# Force AMD64 (Intel/AMD processors)
docker run --platform linux/amd64 -p 7860:7860 huseyincavus/fingemma:latest

# Force ARM64 (Apple Silicon, ARM servers)
docker run --platform linux/arm64 -p 7860:7860 huseyincavus/fingemma:latest
```

### Docker Compose

```bash
# UI Mode
docker-compose --profile ui up

# API Mode  
docker-compose --profile api up

# Both modes
docker-compose --profile default up
```

## Features

- Interactive web interface for finance questions
- REST API with streaming support
- Finance-focused model fine-tuned on financial concepts
- Complete model included in container
- Switch between UI and API modes

## ⚙️ Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_MODE` | `ui` | `ui` for web interface, `api` for REST API |
| `PORT` | `7860` | Port to run the application |
| `SERVER_NAME` | `0.0.0.0` | Server bind address (use `127.0.0.1` for localhost only) |
| `MODEL_ID` | `huseyincavus/gemma-3-270m-finance-merged` | Hugging Face model identifier |
| `LOCAL_MODEL_PATH` | `/app/.cache/huggingface/hub/...` | Local model cache path |

### Volume Mounting

```bash
# Mount custom model cache (optional)
docker run -p 7860:7860 \
  -v /path/to/model/cache:/app/.cache/huggingface \
  huseyincavus/fingemma:latest

# Mount configuration files (optional)
docker run -p 7860:7860 \
  -v /path/to/config:/app/config \
  huseyincavus/fingemma:latest
```

### Resource Limits

```bash
# Set memory and CPU limits
docker run -p 7860:7860 \
  --memory=8g \
  --cpus=4 \
  huseyincavus/fingemma:latest
```

## System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended)
- **Storage**: 6GB free space
- **CPU**: 2 cores (4+ cores recommended)
- **Docker**: 20.10+ 

### Recommended Requirements
- **RAM**: 8-16GB for optimal performance
- **Storage**: 10GB free space (for model cache)
- **CPU**: 4+ cores with AVX2 support
- **GPU**: CUDA-compatible GPU (optional, for faster inference)

### Architecture Support
- ✅ **AMD64**: Intel/AMD x86_64 processors
- ✅ **ARM64**: Apple Silicon, AWS Graviton, ARM servers
- ✅ **Multi-platform**: Automatic architecture detection

## API Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Generate Text Completion
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the current state of the stock market?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

### Streaming Response
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain cryptocurrency basics",
    "max_tokens": 200,
    "stream": true
  }'
```

### API Documentation
When running in API mode, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Troubleshooting

### Common Issues

**Image won't start:**
```bash
# Check Docker logs
docker logs <container_name>

# Verify system requirements
docker run --rm huseyincavus/fingemma:latest python -c "import torch; print(f'PyTorch: {torch.__version__}')"
```

**Out of Memory:**
```bash
# Reduce memory usage with smaller batch size
docker run -p 7860:7860 \
  -e BATCH_SIZE=1 \
  huseyincavus/fingemma:latest
```

**Performance Issues:**
```bash
# Use CPU-only mode if GPU issues
docker run -p 7860:7860 \
  -e CUDA_VISIBLE_DEVICES="" \
  huseyincavus/fingemma:latest
```

**Port Already in Use:**
```bash
# Use different port
docker run -p 8860:7860 huseyincavus/fingemma:latest
# Access at: http://localhost:8860
```

### Architecture-Specific Issues

**Force specific architecture if auto-detection fails:**
```bash
# For Intel/AMD systems
docker pull --platform linux/amd64 huseyincavus/fingemma:latest

# For Apple Silicon/ARM systems  
docker pull --platform linux/arm64 huseyincavus/fingemma:latest
```

## 🛠️ Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/huseyincavusbi/FinGemma.git
cd FinGemma

# Download model
python scripts/download_model.py

# Build image
docker build -t fingemma-local .

# Run locally built image
docker run -p 7860:7860 fingemma-local
```

### Multi-Architecture Build

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 -t your-repo/fingemma:latest --push .
```

## Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete installation instructions for Windows, macOS, and Linux.

## Features

- **Finance-Focused**: Specialized model fine-tuned on financial concepts
- **Interactive Web UI**: User-friendly Gradio interface
- **REST API**: FastAPI with automatic documentation
- **Containerized**: Complete Docker solution with model included
- **Streaming Support**: Real-time response streaming
- **Multi-Architecture**: Support for AMD64 and ARM64
- **Easy Deployment**: One-command Docker setup
- **Configurable**: Environment-based configuration
- **Production Ready**: Docker Compose for orchestration

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built on top of [Google's Gemma](https://ai.google.dev/gemma) foundation model
- Powered by [Hugging Face Transformers](https://huggingface.co/transformers/)
- Web interface using [Gradio](https://gradio.app/)
- API backend with [FastAPI](https://fastapi.tiangolo.com/)
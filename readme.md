# FinGemma - Finance LLM Assistant

A containerized finance-focused language model based on Gemma 3 270M, fine-tuned for financial concepts and discussions.

## Quick Start

```bash
# Run the web interface
docker run -p 7860:7860 huseyincavus/fingemma:latest

# Access at: http://localhost:7860
```

## API Mode

```bash
# Run the API server
docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest

# Access at: http://localhost:8000
```

## Features

- Interactive web interface for finance questions
- REST API with streaming support
- Finance-focused model fine-tuned on financial concepts
- Complete model included in container
- Switch between UI and API modes

## Requirements

- Docker installed
- 8GB RAM recommended
- 5GB free disk space

## Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete installation instructions for Windows, macOS, and Linux.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| APP_MODE | ui | ui for web interface, api for REST API |
| PORT | 7860 | Port to run the application |
| SERVER_NAME | 127.0.0.1 | Server bind address |

## API Endpoints

- GET /health - Health check
- POST /generate - Generate text completion

## License

This project licensed under MIT License. See [LICENSE](LICENSE) for details.
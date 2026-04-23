# Batched Inference Engine - High Performance LLM Inference Engine

Production-ready inference service built on vLLM with intelligent request batching, async streaming, and enterprise-grade architecture for high-throughput LLM deployments.

## Key Features

- **Dynamic Request Batching** - 20ms batch window for optimal GPU utilization with sub-50ms latency overhead
- **Concurrent Streaming** - Handles 100+ simultaneous SSE connections with independent token queues
- **Production Architecture** - Decoupled API layer, batch orchestration, and worker pool for horizontal scaling
- **Real-time Metrics** - Per-request throughput, latency, and token generation rate monitoring
- **Fault Tolerance** - Comprehensive error handling with automatic retry and graceful degradation

## Architecture

```
Client → FastAPI → Batch Queue → Worker Pool → vLLM Engine
           ↓                          ↓
        SSE Stream ← Token Queue ← Async Tasks
```

**Components:**
- `routes.py` - FastAPI endpoints with SSE streaming
- `batch_manager.py` - Thread-safe request aggregation with configurable windows
- `batch_worker.py` - Async worker pool for concurrent batch processing
- `llm_engine.py` - vLLM client with streaming and performance metrics

## Performance

- Throughput scales linearly with batch size up to GPU memory limits
- Concurrent streaming to 100+ clients without blocking
- Adaptive batching balances latency vs GPU utilization
- Real-time monitoring: `tokens=247 | latency=3.42s | speed=72.18 tok/s`  

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start vLLM server
vllm serve Qwen/Qwen2.5-1.5B-Instruct --host 0.0.0.0 --port 5002 --gpu-memory-utilization 0.6

# Terminal 2: Start FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 5001 --reload
```

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI endpoints and SSE streaming
│   ├── core/
│   │   ├── batch_manager.py   # Request batching and queue management
│   │   ├── batch_worker.py    # Async worker pool for batch processing
│   │   └── llm_engine.py      # vLLM client with streaming interface
│   ├── schemas/
│   │   └── models.py          # Pydantic request/response models
│   ├── services/              # Business logic layer
│   └── utilities/             # Helper functions and utilities
├── main.py                    # Application entry point
└── requirements.txt           # Python dependencies
```

## API Usage

**Generate Completion:**
```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing"}'
```

**Response:** Server-Sent Events stream
```
data: Quantum
data:  computing
data:  uses
...
data: [DONE]
```

## Production Deployment

**Docker:** `docker-compose up -d`  
**Kubernetes:** `kubectl apply -f deployment/k8s/`  
**Systemd:** Service files in `deployment/`

## Configuration

Environment variables in `.env`:
- `MODEL_NAME` - HuggingFace model path
- `GPU_MEMORY_UTILIZATION` - GPU allocation (default: 0.6)
- `BATCH_WINDOW_MS` - Batching window in milliseconds (default: 20)
- `MAX_TOKENS` - Max generation length (default: 512)

## Performance Tuning

**Batch Window:**
- Smaller (10-20ms): Lower latency, less batching
- Larger (50-100ms): Higher throughput, more latency

**GPU Memory:**
- Increase for larger batch capacity
- Decrease if encountering OOM errors

## Tech Stack

- vLLM for GPU-accelerated inference
- FastAPI for async web framework
- HTTPX for async HTTP client
- Pydantic for data validation

**Requirements:** Python 3.10+, CUDA 11.8+, 16GB+ GPU memory recommended



## Demo

https://github.com/user-attachments/assets/e69331a0-582a-4aa1-8bbc-39515b0953aa

---



import json
import httpx
from typing import AsyncGenerator
import time
import logging

logger = logging.getLogger(__name__)


class VLLMEngine:
    def __init__(self):
        self.base_url = "http://localhost:5002/v1"
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"  # ✅ Changed model
        self.timeout = httpx.Timeout(30.0, connect=5.0)
    
    async def generate_stream(self, user_prompt: str) -> AsyncGenerator[str, None]:
        messages = [
            {
                "role": "system",
                "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."  # ✅ Qwen's system prompt
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ]
        
        start_time = time.time()
        token_count = 0
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model_name,
                        "messages": messages,
                        "max_tokens": 512,  # ✅ Increased for better responses
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "stream": True,
                    },
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                text = delta.get("content", "")
                                if text:
                                    token_count += 1
                                    yield text
                        except json.JSONDecodeError:
                            continue

            # ✅ AFTER STREAM COMPLETES (SUCCESS CASE)
            end_time = time.time()
            latency = end_time - start_time
            tokens_per_sec = token_count / latency if latency > 0 else 0

            logger.info(
                f"Request completed | tokens={token_count} | latency={latency:.2f}s | speed={tokens_per_sec:.2f} tok/s"
            )

        except httpx.TimeoutException:
            logger.error("Timeout from vLLM")  # ✅ LOG ERROR
            yield "[ERROR] Timeout from vLLM"

        except httpx.ConnectError:
            logger.error("Connection error to vLLM")  # ✅ LOG ERROR
            yield "[ERROR] Cannot connect to vLLM"

        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP error from vLLM: {exc.response.status_code}")  # ✅ LOG ERROR
            yield f"[ERROR] HTTP {exc.response.status_code}"

        except Exception as exc:
            logger.error(f"Unexpected error: {str(exc)}")  # ✅ LOG ERROR
            yield f"[ERROR] {str(exc)}"
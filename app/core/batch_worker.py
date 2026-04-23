import asyncio
from app.core.batch_manager import BatchManager
from app.core.llm_engine import VLLMEngine

batch_manager = BatchManager()
engine = VLLMEngine()


async def batch_worker():
    while True:
        batch = await batch_manager.get_batch()

        if not batch:
            continue

        tasks = []
        for req in batch:
            tasks.append(handle_request(req))

        await asyncio.gather(*tasks)


async def handle_request(req):
    async for token in engine.generate_stream(req.prompt):
        await req.queue.put(token)

    await req.queue.put("[DONE]")
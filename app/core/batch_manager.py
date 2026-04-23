import asyncio
from typing import List

class BatchRequest:
    def __init__(self, prompt):
        self.prompt = prompt
        self.queue = asyncio.Queue()


class BatchManager:
    def __init__(self):
        self.queue: List[BatchRequest] = []
        self.lock = asyncio.Lock()
        self.batch_window = 0.02

    async def add_request(self, request: BatchRequest):
        async with self.lock:
            self.queue.append(request)

    async def get_batch(self):
        await asyncio.sleep(self.batch_window)

        async with self.lock:
            batch = self.queue
            self.queue = []

        return batch